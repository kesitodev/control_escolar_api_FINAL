from django.shortcuts import render, get_object_or_404
from django.db.models import *
from django.db import transaction
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json

from control_escolar_desit_api.serializers import UserSerializer, AlumnoSerializer
from control_escolar_desit_api.models import Alumnos, User

class AlumnosAll(generics.CreateAPIView):
    # Verificar si el usuario esta autenticado
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active = 1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        return Response(lista, 200)

class AlumnosView(generics.CreateAPIView):
    # Permisos por método (sobrescribe el comportamiento default)
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    # Obtener alumno por ID
    def get(self, request, *args, **kwargs):
        # Se obtiene el ID de los parametros de la URL (?id=1)
        alumno = get_object_or_404(Alumnos, id = request.GET.get("id"))
        alumno_data = AlumnoSerializer(alumno, many=False).data
        return Response(alumno_data, 200)

    # Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            # Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            # Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"}, 400)

            user = User.objects.create(
                username = email,
                email = email,
                first_name = first_name,
                last_name = last_name,
                is_active = 1
            )

            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # Create a profile for the user
            alumno = Alumnos.objects.create(
                user=user,
                matricula= request.data["matricula"],
                curp= request.data["curp"].upper(),
                rfc= request.data["rfc"].upper(),
                fecha_nacimiento= request.data["fecha_nacimiento"],
                edad= request.data["edad"],
                telefono= request.data["telefono"],
                ocupacion= request.data["ocupacion"]
            )
            alumno.save()

            return Response({"Alumno creado con ID: ": alumno.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar datos del alumno
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # Nota: Aquí buscas el ID en el body del JSON (request.data)
        alumno = get_object_or_404(Alumnos, id=request.data.get("id"))
        user = alumno.user

        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.username = request.data.get("email", user.username)
        user.save()

        alumno.matricula = request.data.get("matricula", alumno.matricula)
        alumno.curp = request.data.get("curp", alumno.curp).upper()
        alumno.rfc = request.data.get("rfc", alumno.rfc).upper()
        alumno.fecha_nacimiento = request.data.get("fecha_nacimiento", alumno.fecha_nacimiento)
        alumno.edad = request.data.get("edad", alumno.edad)
        alumno.telefono = request.data.get("telefono", alumno.telefono)
        alumno.ocupacion = request.data.get("ocupacion", alumno.ocupacion)
        alumno.save()

        return Response({"message":"Alumno actualizado", "alumno": AlumnoSerializer(alumno).data}, 200)

    # Eliminar alumno
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        try:
            alumno.user.delete()
            return Response({"details":"Alumno eliminado"}, 200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"}, 400)


class AlumnosAll(generics.CreateAPIView):
    # Verificar si el usuario esta autenticado
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active=True).order_by("id")
        lista_alumnos = AlumnoSerializer(alumnos, many=True).data
        return Response(lista_alumnos, 200)