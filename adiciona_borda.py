import os
import argparse
from PIL import Image, ImageDraw


# def exibir_borda(borda):
#     borda = Image.open(os.path.join(diretorio_script, "borda.png"))
#     borda.show()

# Função para sobrepor a borda em uma imagem
def sobrepor_borda(imagem, borda, alinhamento):
    if alinhamento == "up":
        posicao_y = 0
    elif alinhamento == "down":
        posicao_y = borda.height - imagem.height
    else:  # Padrão: centralizar
        posicao_y = (borda.height - imagem.height) // 2

    nova_imagem = Image.new('RGBA', borda.size)
    #nova_imagem.paste(imagem, ((borda.width - imagem.width) // 2, (borda.height - imagem.height) // 2), imagem)
    nova_imagem.paste(imagem, ((borda.width - imagem.width) // 2, posicao_y), imagem)
    nova_imagem.paste(borda, (0, 0), borda)
    return nova_imagem


# Configurar o parser de argumentos
parser = argparse.ArgumentParser(description="Adicionar borda a imagens")
parser.add_argument("alinhamento", nargs="?", choices=["up", "down"], default=None, help="Alinhamento da imagem (up, down)")

# Diretório do script
diretorio_script = os.path.dirname(os.path.realpath(__file__))
# Caminho para a pasta de fotos
pasta_fotos = os.path.join(diretorio_script, "fotos")
# Caminho para a pasta de fotos com borda
pasta_com_borda = os.path.join(diretorio_script, "com_borda")

# Verificar se a pasta com_borda existe, se não, criar
if not os.path.exists(pasta_com_borda):
    os.makedirs(pasta_com_borda)

# Carregar a imagem da borda
borda = Image.open(os.path.join(diretorio_script, "borda.png")).convert("RGBA")
#nova_borda = borda.convert("RGBA")
#nova_borda.show()

# Contador para nomear as imagens
contador = 1

# Parse dos argumentos
args = parser.parse_args()

# Iterar sobre os arquivos na pasta de fotos
for arquivo in os.listdir(pasta_fotos):
    if arquivo.endswith(".png") or arquivo.endswith(".jpg"):
        # Carregar a imagem atual
        caminho_imagem = os.path.join(pasta_fotos, arquivo)
        imagem_atual = Image.open(caminho_imagem).convert("RGBA")

        # Redimensionar a imagem para que sua largura coincida com a largura da borda
        proporcao = borda.width / imagem_atual.width
        nova_altura = int(imagem_atual.height * proporcao)
        imagem_redimensionada = imagem_atual.resize((borda.width, nova_altura))

        # Sobrepor a borda na imagem atual
        imagem_final = sobrepor_borda(imagem_redimensionada, borda, args.alinhamento)
        
        # Salvar a imagem final com a extensão PNG
        # caminho_imagem_final = os.path.join(pasta_com_borda, "com_borda_" + os.path.splitext(arquivo)[0] + ".png")
        # imagem_final.save(caminho_imagem_final)

        # Salvar a imagem final na pasta com_borda
        nome_arquivo_final = "foto{:02d}.png".format(contador)
        print("Salvando arquivo: %s" % nome_arquivo_final)
        caminho_imagem_final = os.path.join(pasta_com_borda, nome_arquivo_final)
        imagem_final.save(caminho_imagem_final)
        
        # Incrementar o contador
        contador += 1        

