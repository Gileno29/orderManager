from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import time




class EncontrarVogalView(APIView):
    permission_classes = [AllowAny]

    def encontrar_vogal(self,string):
        vogais = "aeiouAEIOU"
        consoantes = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
        
        # Variáveis para rastrear o estado
        vogais_vistas = set()  # Conjunto de vogais já vistas
        vogais_unicas = set()  # Conjunto de vogais únicas
        consoante_anterior = False  # Flag para indicar se o caractere anterior foi uma consoante
        vogal_antecessora = False  # Flag para indicar se o caractere anterior à consoante foi uma vogal

        for char in string:
            if char in vogais:
                # Verifica se a vogal já foi vista antes
                if char in vogais_vistas:
                    # Se já foi vista, remove das vogais únicas
                    if char in vogais_unicas:
                        vogais_unicas.remove(char)
                else:
                    # Se não foi vista, adiciona ao conjunto de vogais vistas e únicas
                    vogais_vistas.add(char)
                    vogais_unicas.add(char)
                
                # Verifica se a vogal atende às condições
                if consoante_anterior and vogal_antecessora and char in vogais_unicas:
                    return char  # Retorna a vogal que atende às condições
                
                # Reseta as flags após processar uma vogal
                consoante_anterior = False
                vogal_antecessora = False

            elif char in consoantes:
                # Verifica se o caractere anterior foi uma vogal
                if len(vogais_vistas) > 0:
                    vogal_antecessora = True
                consoante_anterior = True
            else:
                # Reseta as flags para caracteres que não são vogais nem consoantes
                consoante_anterior = False
                vogal_antecessora = False

        return None  # Retorna None se nenhuma vogal atender às condições

    def post(self, request):
    
        string = request.data.get('string', '')

        if not string:
            return Response(
                {"error": "A string não foi fornecida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Inicia o cronômetro
        inicio = time.time()

        # Encontra a vogal
        vogal = self.encontrar_vogal(string)

        # Calcula o tempo total
        tempo_total = (time.time() - inicio) * 1000  

       
        if vogal:
            return Response({
                "string": string,
                "vogal": vogal,
                "tempoTotal": f"{tempo_total:.2f}ms"
            })
        else:
            return Response({
                "string": string,
                "vogal": None,
                "tempoTotal": f"{tempo_total:.2f}ms"
            })