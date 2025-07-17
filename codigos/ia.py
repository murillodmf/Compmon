import random
import functions
import copy

class PokemonAI:
    def __init__(self, nivel_dificuldade="avancado"):
        self.nivel_dificuldade = nivel_dificuldade
        self.historico_ataques_oponente = []

    def escolher_ataque(self, pokemon_ia, pokemon_oponente):
        if self.nivel_dificuldade == "iniciante":
            return self.escolher_ataque_facil(pokemon_ia)
        elif self.nivel_dificuldade == "intermediario":
            return self.escolher_ataque_intermediario(pokemon_ia, pokemon_oponente)
        elif self.nivel_dificuldade == "avancado":
            return self.escolher_ataque_avancado(pokemon_ia, pokemon_oponente)
        else:
            return self.escolher_ataque_facil(pokemon_ia)

    def escolher_ataque_facil(self, pokemon_ia):
        return random.choice(pokemon_ia.ataques)

    def escolher_ataque_intermediario(self, pokemon_ia, pokemon_oponente):
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

    def evaluate_state(self, pokemon_ia, pokemon_oponente):
        pontuacao_ia = (pokemon_ia.hp / pokemon_ia.hpmax) * 100
        pontuacao_oponente = (pokemon_oponente.hp / pokemon_oponente.hpmax) * 100
        
        pontuacao_ia += (pokemon_ia.atk + pokemon_ia.defesa) * 0.1
        pontuacao_oponente += (pokemon_oponente.atk + pokemon_oponente.defesa) * 0.1

        return pontuacao_ia - pontuacao_oponente

    def simulate_move(self, ataque, atacante_sim, defensor_sim):
        if not ataque.dano:
            return 0

        multiplicador = functions.vantagens(ataque, defensor_sim)
        dano_simulado = ataque.calcular_dano(atacante_sim, defensor_sim, multiplicador)
        return dano_simulado

    def escolher_ataque_avancado(self, pokemon_ia, pokemon_oponente):
        melhor_ataque_final = None
        melhor_pior_cenario = -float('inf')

        for meu_ataque in pokemon_ia.ataques:
            ia_clone = pokemon_ia.copy()
            oponente_clone = pokemon_oponente.copy()
            
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

            if pior_cenario_para_mim > melhor_pior_cenario:
                melhor_pior_cenario = pior_cenario_para_mim
                melhor_ataque_final = meu_ataque

        return melhor_ataque_final

    def aprender_com_oponente(self, ataque_oponente):
        pass

    def salvar_memoria_da_batalha(self):
        pass