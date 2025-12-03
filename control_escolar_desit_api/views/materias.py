from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from control_escolar_desit_api.serializers import MateriaSerializer
from control_escolar_desit_api.models import Materias, Administradores, Maestros, BearerTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime

class MateriasView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def format_time_for_django(self, time_str):
        try:
            return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M:%S")
        except (ValueError, TypeError):
            return time_str

    # 1. GET: Obtener una materia por ID
    def get(self, request, format=None):
        try:
            id = request.query_params['id']
            materia = Materias.objects.get(id=id)
            serializer = MateriaSerializer(materia)
            data = serializer.data
            
            if "dias" in data and data["dias"]:
                try:
                    data["dias"] = json.loads(data["dias"])
                except:
                    data["dias"] = []
            
            return Response(data, status=status.HTTP_200_OK)
        except Materias.DoesNotExist:
            return Response({'error': 'Materia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 2. POST: Registrar Materia (Solo Admin)
    @transaction.atomic
    def post(self, request, format=None):
        if not Administradores.objects.filter(user=request.user).exists():
            return Response({'error': 'No tienes permisos de administrador'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()

        # A) Convertir Array de Días a JSON String
        if 'dias' in data:
            data['dias'] = json.dumps(data['dias'])

        if 'hora_inicio' in data:
            data['hora_inicio'] = self.format_time_for_django(data['hora_inicio'])
        if 'hora_fin' in data:
            data['hora_fin'] = self.format_time_for_django(data['hora_fin'])

        serializer = MateriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. PUT: Actualizar Materia (Solo Admin)
    @transaction.atomic
    def put(self, request, format=None):
        if not Administradores.objects.filter(user=request.user).exists():
            return Response({'error': 'No tienes permisos de administrador'}, status=status.HTTP_403_FORBIDDEN)

        try:
            materia = Materias.objects.get(id=request.data['id'])
            
            data = request.data.copy()
            if 'dias' in data and isinstance(data['dias'], list):
                data['dias'] = json.dumps(data['dias'])
            
            if 'hora_inicio' in data:
                data['hora_inicio'] = self.format_time_for_django(data['hora_inicio'])
            if 'hora_fin' in data:
                data['hora_fin'] = self.format_time_for_django(data['hora_fin'])

            serializer = MateriaSerializer(materia, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Materias.DoesNotExist:
            return Response({'error': 'Materia no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # 4. DELETE: Eliminar Materia (Solo Admin)
    @transaction.atomic
    def delete(self, request, format=None):
        if not Administradores.objects.filter(user=request.user).exists():
            return Response({'error': 'No tienes permisos de administrador'}, status=status.HTTP_403_FORBIDDEN)

        try:
            materia = Materias.objects.get(id=request.query_params['id'])
            materia.delete()
            return Response({'message': 'Materia eliminada correctamente'}, status=status.HTTP_200_OK)
        except Materias.DoesNotExist:
            return Response({'error': 'Materia no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class MateriasAll(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        es_admin = Administradores.objects.filter(user=request.user).exists()
        es_maestro = Maestros.objects.filter(user=request.user).exists()

        if not (es_admin or es_maestro):
            return Response({'error': 'No tienes permisos para ver esta lista'}, status=status.HTTP_403_FORBIDDEN)

        materias = Materias.objects.all().order_by('-creation')
        lista_data = MateriaSerializer(materias, many=True).data

        # --- AQUÍ ESTÁ EL ARREGLO ---
        for mat in lista_data:
            if "dias" in mat and mat["dias"]:
                try:
                    mat["dias"] = json.loads(mat["dias"])
                except:
                    mat["dias"] = []
            
           
            if "profesor" in mat:
                try:
                    maestro_obj = Maestros.objects.get(id=mat["profesor"])
                    nombre_completo = f"{maestro_obj.user.first_name} {maestro_obj.user.last_name}"
                    mat["profesor_nombre"] = nombre_completo
                except Maestros.DoesNotExist:
                    mat["profesor_nombre"] = "Maestro no encontrado"
            else:
                mat["profesor_nombre"] = "Sin asignar"
        
        return Response(lista_data, status=status.HTTP_200_OK)