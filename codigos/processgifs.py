from PIL import Image
import os

print("Diretorio atual:", os.getcwd())

def process_gifs(input_folder, output_folder):
    # Verifica se a pasta de saída existe, se não, cria
    os.makedirs(output_folder, exist_ok=True)

    # Percorre todos os arquivos no diretório de entrada
    for filename in os.listdir(input_folder):
        if filename.endswith(".gif"):
            gif_path = os.path.join(input_folder, filename)
            gif = Image.open(gif_path)

            # Cria uma subpasta para os quadros deste GIF
            gif_name = os.path.splitext(filename)[0]
            gif_output_folder = os.path.join(output_folder, gif_name)
            os.makedirs(gif_output_folder, exist_ok=True)

            # Extrai e salva cada quadro
            for frame in range(gif.n_frames):
                gif.seek(frame)
                frame_image = gif.convert("RGBA")
                frame_filename = f"frame_{frame:02d}.png"
                frame_image.save(os.path.join(gif_output_folder, frame_filename))

            print(f"Quadros de {filename} salvos com sucesso na pasta {gif_output_folder}!")

# Exemplo de uso com caminho relativo
input_folder = "images/battle/gifsbattle"  # Caminho relativo do script até a pasta 'gifs'
output_folder = "images/battle/gifsframes"  # Caminho relativo para a pasta onde os quadros serão salvos

if not os.path.exists(input_folder):
    print(f"Erro: A pasta de entrada '{input_folder}' não existe.")
else:
    print(f"A pasta de entrada '{input_folder}' foi encontrada.")

process_gifs(input_folder, output_folder)
