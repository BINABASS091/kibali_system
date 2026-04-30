from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import FileResponse
from weasyprint import HTML, CSS
from rest_framework_simplejwt.tokens import RefreshToken
import io
import os
from datetime import datetime, timedelta

from .models import Permit, KibaliUser
from .serializers import PermitSerializer, LoginSerializer


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
        
        # Generate PDF
        try:
            html_content = render_to_string('permit.html', {
                'permit': permit
            })
            
            # Create PDF using WeasyPrint
            html = HTML(string=html_content, base_url='.')
            pdf_bytes = html.write_pdf()
            
            # Save PDF file
            os.makedirs('media/permits', exist_ok=True)
            pdf_path = f'media/permits/{permit.permit_number}.pdf'
            
            with open(pdf_path, 'wb') as f:
                f.write(pdf_bytes)
            
            permit.pdf_file = f'permits/{permit.permit_number}.pdf'
            permit.save()
        
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
        
        if not permit.pdf_file:
            return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)
        
        pdf_path = permit.pdf_file.path
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf', as_attachment=True, filename=f'{permit.permit_number}.pdf')
    
    except Permit.DoesNotExist:
        return Response({'error': 'Permit not found'}, status=status.HTTP_404_NOT_FOUND)
