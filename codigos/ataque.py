# Em ataque.py

class ataque:
    def __init__(self, nome, tipo, dano, velocidade, efeito, quantidade):
        self.nome = nome
        self.tipo = tipo
        self.dano = dano
        self.velocidade = velocidade
        self.efeito = efeito
        self.quantidade = quantidade

    def calcular_dano(self, jogador, adversario, multiplicador):
        # A fórmula original tem um problema: se a velocidade do adversário for muito maior,
        # o dano pode ficar muito baixo. Vamos ajustar para ser mais estável.
        fator_velocidade = (jogador.velocidade / adversario.velocidade)
        # Limita o fator de velocidade para que não penalize ou beneficie demais
        fator_velocidade = max(0.5, min(fator_velocidade, 1.5))
        
        return (self.dano * multiplicador) * (jogador.atk / adversario.defesa) * fator_velocidade

    # --- MÉTODO NOVO ADICIONADO ---
    def copy(self):
        """Cria uma cópia exata deste objeto de ataque."""
        return ataque(self.nome, self.tipo, self.dano, self.velocidade, self.efeito, self.quantidade)