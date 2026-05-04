from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.http import FileResponse
from weasyprint import HTML, CSS
from rest_framework_simplejwt.tokens import RefreshToken
import base64
import io
import os
from pathlib import Path
import qrcode

from .models import Permit, KibaliUser
from .serializers import PermitSerializer, LoginSerializer


def _svg_data_uri(svg_markup):
    encoded = base64.b64encode(svg_markup.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{encoded}'


def _create_stamp_fallback():
    """Simple fallback stamp if no PNG file exists."""
    svg = """
    <svg xmlns='http://www.w3.org/2000/svg' width='220' height='220' viewBox='0 0 220 220'>
      <circle cx='110' cy='110' r='100' fill='none' stroke='#8f1d1d' stroke-width='8'/>
      <circle cx='110' cy='110' r='78' fill='none' stroke='#8f1d1d' stroke-width='3' stroke-dasharray='3,5'/>
      <text x='110' y='92' text-anchor='middle' font-family='Arial' font-size='14' fill='#8f1d1d'>SEREKALI YA</text>
      <text x='110' y='112' text-anchor='middle' font-family='Arial' font-size='14' fill='#8f1d1d'>MAPINDUZI</text>
      <text x='110' y='132' text-anchor='middle' font-family='Arial' font-size='14' fill='#8f1d1d'>ZANZIBAR</text>
    </svg>
    """
    return _svg_data_uri(svg)


def _create_signature_fallback():
    """Simple fallback signature if no image exists."""
    svg = """
    <svg xmlns='http://www.w3.org/2000/svg' width='360' height='90' viewBox='0 0 360 90'>
      <path d='M10 58 C38 12, 72 75, 108 38 C124 22, 140 44, 156 56 C176 70, 196 20, 226 34 C244 42, 258 66, 284 58 C298 54, 318 36, 346 48'
            stroke='#1f2937' stroke-width='4' fill='none' stroke-linecap='round'/>
      <path d='M248 28 C260 14, 274 14, 286 30' stroke='#1f2937' stroke-width='3' fill='none' stroke-linecap='round'/>
    </svg>
    """
    return _svg_data_uri(svg)


def _create_emblem_fallback():
        """Simple coat-of-arms style fallback for header corners."""
        svg = """
        <svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'>
            <circle cx='60' cy='60' r='55' fill='none' stroke='#b98b2f' stroke-width='4'/>
            <circle cx='60' cy='60' r='44' fill='none' stroke='#d1a54a' stroke-width='2'/>
            <path d='M60 24 L75 44 L60 90 L45 44 Z' fill='#b98b2f' opacity='0.88'/>
            <circle cx='60' cy='50' r='10' fill='#7b5a1a'/>
            <text x='60' y='109' text-anchor='middle' font-family='Arial' font-size='9' fill='#7b5a1a'>SMZ</text>
        </svg>
        """
        return _svg_data_uri(svg)


def _load_image_data_uri(image_path):
    if not image_path.exists():
        return None

    ext = image_path.suffix.lower().lstrip('.')
    mime = 'image/png' if ext == 'png' else f'image/{ext}'
    encoded = base64.b64encode(image_path.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{encoded}'


def _build_qr_data_uri(permit):
    verify_base_url = getattr(settings, 'VERIFY_BASE_URL', 'http://localhost:5173').rstrip('/')
    verify_url = f'{verify_base_url}/verify/{permit.permit_number}'
    payload = (
        f'Permit: {permit.permit_number}\n'
        f'Applicant: {permit.jina}\n'
        f'Issued: {permit.tarehe_kutolewa}\n'
        f'Verify: {verify_url}'
    )

    qr = qrcode.QRCode(version=1, box_size=5, border=1)
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}', verify_url


def generate_permit_pdf(permit):
    """Render a permit PDF and persist it on the model."""
    assets_dir = Path(settings.BASE_DIR) / 'media' / 'assets'
    static_bg_path = Path(settings.BASE_DIR) / 'static' / 'kibali-bg.png'
    background_path = static_bg_path if static_bg_path.exists() else assets_dir / 'kibali-bg.png'
    background_url = background_path.as_uri() if background_path.exists() else ''

    field_positions = {
        'applicant': {'top': '33mm', 'left': '43mm'},
        'construction': {'top': '41mm', 'left': '43mm'},
        'location': {'top': '49mm', 'left': '43mm'},
        'shehia': {'top': '57mm', 'left': '43mm'},
        'kaskazini': {'top': '73mm', 'left': '40mm'},
        'mashariki': {'top': '81mm', 'left': '40mm'},
        'magharibi': {'top': '89mm', 'left': '40mm'},
        'kusini': {'top': '97mm', 'left': '40mm'},
        'upana': {'top': '108mm', 'left': '32mm'},
        'urefu': {'top': '116mm', 'left': '32mm'},
        'tarehe_kutolewa': {'top': '125mm', 'left': '40mm'},
        'tarehe_mwisho': {'top': '133mm', 'left': '40mm'},
    }

    html_content = render_to_string('permit.html', {
        'permit': permit,
        'background_url': background_url,
        'field_positions': field_positions,
    })

    html = HTML(string=html_content, base_url='.')
    pdf_bytes = html.write_pdf()

    pdf_name = f'{permit.permit_number}.pdf'
    permit.pdf_file.save(pdf_name, ContentFile(pdf_bytes), save=True)
    return pdf_bytes


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_permit(request, permit_number):
    """Public verification endpoint used by QR scans."""
    try:
        permit = Permit.objects.get(permit_number=permit_number)
    except Permit.DoesNotExist:
        return Response({
            'found': False,
            'permit_number': permit_number,
            'status': 'not_found',
            'message': 'Kibali hakikupatikana.'
        }, status=status.HTTP_404_NOT_FOUND)

    today = timezone.localdate()
    is_valid = permit.tarehe_mwisho >= today
    state = 'valid' if is_valid else 'expired'

    return Response({
        'found': True,
        'status': state,
        'is_valid': is_valid,
        'permit': {
            'id': permit.id,
            'permit_number': permit.permit_number,
            'jina': permit.jina,
            'aina': permit.get_aina_display(),
            'pahala': permit.pahala,
            'shehia': permit.shehia,
            'tarehe_kutolewa': permit.tarehe_kutolewa,
            'tarehe_mwisho': permit.tarehe_mwisho,
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handle user login and return JWT token
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate JWT token using simplejwt
            refresh = RefreshToken.for_user(user)
            
            # Get user role
            try:
                kibali_user = KibaliUser.objects.get(user=user)
                role = kibali_user.role
            except KibaliUser.DoesNotExist:
                role = 'officer'
            
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': role,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_permit(request):
    """
    Create a new permit and generate PDF
    """
    serializer = PermitSerializer(data=request.data)
    
    if serializer.is_valid():
        permit = serializer.save(created_by=request.user)
        
        try:
            generate_permit_pdf(permit)
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
        
        return Response(PermitSerializer(permit).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_permits(request):
    """
    List all permits (admin only) or user's permits (officer)
    """
    try:
        kibali_user = KibaliUser.objects.get(user=request.user)
        role = kibali_user.role
    except KibaliUser.DoesNotExist:
        role = 'officer'
    
    if role == 'admin':
        permits = Permit.objects.all()
    else:
        permits = Permit.objects.filter(created_by=request.user)
    
    serializer = PermitSerializer(permits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_permit_detail(request, permit_id):
    """
    Get a single permit detail
    """
    try:
        permit = Permit.objects.get(id=permit_id)
        
        # Check if user has permission
        try:
            kibali_user = KibaliUser.objects.get(user=request.user)
            role = kibali_user.role
        except KibaliUser.DoesNotExist:
            role = 'officer'
        
        if role != 'admin' and permit.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PermitSerializer(permit)
        return Response(serializer.data)
    
    except Permit.DoesNotExist:
        return Response({'error': 'Permit not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_permit_pdf(request, permit_id):
    """
    Download permit PDF
    """
    try:
        permit = Permit.objects.get(id=permit_id)
        
        # Check if user has permission
        try:
            kibali_user = KibaliUser.objects.get(user=request.user)
            role = kibali_user.role
        except KibaliUser.DoesNotExist:
            role = 'officer'
        
        if role != 'admin' and permit.created_by != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        if not permit.pdf_file or not default_storage.exists(permit.pdf_file.name):
            try:
                generate_permit_pdf(permit)
            except Exception as e:
                print(f"Error regenerating PDF: {str(e)}")
                return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pdf_path = permit.pdf_file.path
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf', as_attachment=True, filename=f'{permit.permit_number}.pdf')
    
    except Permit.DoesNotExist:
        return Response({'error': 'Permit not found'}, status=status.HTTP_404_NOT_FOUND)
