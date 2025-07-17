# Em criatura.py

from efeitos import efeitos
from ataque import ataque
import functions

class criatura:
    def __init__(self, nome, tipo, hp, atk, defesa, velocidade, ataques, image_path):
        self.nome = nome
        self.tipo = tipo
        self.hp = hp
        self.atk = atk
        self.defesa = defesa
        self.velocidade = velocidade
        self.hpmax = hp
        self.ataques = ataques
        self.image_path = image_path
        self.efeitosativos = efeitos()
        self.is_ai = False
        self.ai = None

    def receber_dano(self, dano):
        dano_final = max(1, round(dano)) # Garante que o dano seja pelo menos 1 e arredondado
        if self.hp - dano_final < 0:
            self.hp = 0
        else:
            self.hp -= dano_final
        print(f"{self.nome} recebeu {dano_final} de dano. HP restante: {self.hp}\n")

    # --- MÉTODO NOVO ADICIONADO ---
    def copy(self):
        """Cria uma cópia exata (clone) desta criatura para simulação."""
        # Copia os ataques um por um usando o método .copy() de cada ataque
        ataques_copiados = [atk.copy() for atk in self.ataques]
        
        clone = criatura(
            self.nome, self.tipo, self.hp, self.atk, self.defesa,
            self.velocidade, ataques_copiados, self.image_path
        )
        clone.hpmax = self.hpmax
        # Importante: O clone não precisa da IA ou dos efeitos para a simulação de dano
        clone.is_ai = self.is_ai 
        
        return clone