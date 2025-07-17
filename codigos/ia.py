import random
import functions
import copy
import json
import os

class PokemonAI:
    def __init__(self, nivel_dificuldade="avancado"):
        self.nivel_dificuldade = nivel_dificuldade
        
        # Atributos para o aprendizado
        self.movimentos_nesta_batalha = []
        self.memoria_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'memoria_ia.json')
        self.memoria_carregada = self._carregar_memoria()

    def _carregar_memoria(self):
        """Carrega a memória do arquivo JSON. Se não existir, retorna um dicionário vazio."""
        try:
            with open(self.memoria_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def escolher_ataque(self, pokemon_ia, pokemon_oponente):
        """Ponto de entrada que escolhe o ataque e registra a escolha para aprendizado futuro."""
        ataque_escolhido = None
        if self.nivel_dificuldade == "iniciante":
            ataque_escolhido = self.escolher_ataque_facil(pokemon_ia)
        elif self.nivel_dificuldade == "intermediario":
            ataque_escolhido = self.escolher_ataque_intermediario(pokemon_ia, pokemon_oponente)
        elif self.nivel_dificuldade == "avancado":
            ataque_escolhido = self.escolher_ataque_avancado(pokemon_ia, pokemon_oponente)
        
        if ataque_escolhido is None:
            ataque_escolhido = random.choice(pokemon_ia.ataques)
            
        # Registra o nome do ataque escolhido para análise pós-batalha
        self.movimentos_nesta_batalha.append(ataque_escolhido.nome)
        
        return ataque_escolhido
    
    def escolher_ataque_facil(self, pokemon_ia):
        """IA NÍVEL 1: Totalmente aleatória."""
        return random.choice(pokemon_ia.ataques)

    def escolher_ataque_intermediario(self, pokemon_ia, pokemon_oponente):
        """IA NÍVEL 2: Gulosa. Escolhe o ataque que causa o maior dano bruto."""
        melhor_ataque = None
        maior_dano = -1

        for ataque in pokemon_ia.ataques:
            if not ataque.dano:
                continue
            dano_simulado = self.simulate_move(ataque, pokemon_ia, pokemon_oponente)
            if dano_simulado > maior_dano:
                maior_dano = dano_simulado
                melhor_ataque = ataque
        
        if melhor_ataque is None:
            return self.escolher_ataque_facil(pokemon_ia)
            
        return melhor_ataque

    def escolher_ataque_avancado(self, pokemon_ia, pokemon_oponente):
        """IA AVANÇADA - Combina Minimax com a memória de aprendizado."""
        melhor_ataque_final = None
        melhor_pontuacao_final = -float('inf')

        for meu_ataque in pokemon_ia.ataques:
            ia_clone = pokemon_ia.copy()
            oponente_clone = pokemon_oponente.copy()
            
            # 1. Simulação Minimax
            dano_que_eu_causo = self.simulate_move(meu_ataque, ia_clone, oponente_clone)
            oponente_clone.hp -= dano_que_eu_causo

            if oponente_clone.hp <= 0:
                return meu_ataque
            
            pior_cenario_para_mim = float('inf')

            for ataque_inimigo in oponente_clone.ataques:
                ia_depois_do_contra_ataque = ia_clone.copy()
                dano_que_eu_sofro = self.simulate_move(ataque_inimigo, oponente_clone, ia_depois_do_contra_ataque)
                ia_depois_do_contra_ataque.hp -= dano_que_eu_sofro
                
                nota_do_cenario = self.evaluate_state(ia_depois_do_contra_ataque, oponente_clone)
                
                if nota_do_cenario < pior_cenario_para_mim:
                    pior_cenario_para_mim = nota_do_cenario

            # 2. Pega a Pontuação Histórica do ataque
            dados_ataque = self.memoria_carregada.get(meu_ataque.nome, {'usos_em_vitorias': 0, 'usos_em_derrotas': 0})
            vitorias = dados_ataque['usos_em_vitorias']
            derrotas = dados_ataque['usos_em_derrotas']
            total_usos = vitorias + derrotas
            
            pontuacao_historica = (vitorias + 1) / (total_usos + 2) 

            # 3. Combina as pontuações
            pontuacao_final_combinada = (pior_cenario_para_mim * 0.7) + ((pontuacao_historica * 100 - 50) * 0.3)

            if pontuacao_final_combinada > melhor_pontuacao_final:
                melhor_pontuacao_final = pontuacao_final_combinada
                melhor_ataque_final = meu_ataque
        
        return melhor_ataque_final

    def evaluate_state(self, pokemon_ia, pokemon_oponente):
        pontuacao_ia = (pokemon_ia.hp / pokemon_ia.hpmax) * 100
        pontuacao_oponente = (pokemon_oponente.hp / pokemon_oponente.hpmax) * 100
        pontuacao_ia += (pokemon_ia.atk + pokemon_ia.defesa) * 0.1
        pontuacao_oponente += (pokemon_oponente.atk + pokemon_oponente.defesa) * 0.1
        return pontuacao_ia - pontuacao_oponente

    def simulate_move(self, ataque, atacante_sim, defensor_sim):
        if not ataque.dano: return 0
        multiplicador = functions.vantagens(ataque, defensor_sim)
        dano_simulado = ataque.calcular_dano(atacante_sim, defensor_sim, multiplicador)
        return dano_simulado

    def aprender_com_oponente(self, ataque_oponente):
        pass

    def salvar_memoria_da_batalha(self, resultado_batalha):
        """
        Atualiza a memória da IA com base no resultado da batalha.
        'resultado_batalha' deve ser "vitoria" ou "derrota".
        """
        memoria_atual = self._carregar_memoria()

        for nome_ataque in self.movimentos_nesta_batalha:
            if nome_ataque not in memoria_atual:
                memoria_atual[nome_ataque] = {'usos_em_vitorias': 0, 'usos_em_derrotas': 0}

            if resultado_batalha == "vitoria":
                memoria_atual[nome_ataque]['usos_em_vitorias'] += 1
            elif resultado_batalha == "derrota":
                memoria_atual[nome_ataque]['usos_em_derrotas'] += 1
        
        with open(self.memoria_path, 'w') as f:
            json.dump(memoria_atual, f, indent=4)
        
        print(f"IA salvou o aprendizado da batalha. Resultado: {resultado_batalha}")