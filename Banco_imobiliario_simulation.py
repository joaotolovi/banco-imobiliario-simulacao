import random

'''
Funções de compra para cada tipo de player.
'''
def buy_fun_i(property_, player):
    '''Funções de compra do player impulsivo
    '''
    return True


def buy_fun_e(property_, player):
    '''Funções de compra do player exigente
    '''
    if property_['rent_value'] > 50:
        return True
    return False


def buy_fun_c(property_, player):
    '''Funções de compra do player cauteloso
    '''
    if player['money'] - property_['price'] > 80:
        return True
    return False


def buy_fun_a(property_, player):
    '''Funções de compra do player aleatório
    '''    
    return random.choice([True, False])


class BancoImobiliario:
    """Classe que cria e gerencia a simulação do Banco Imobiliario
    """
    def __init__(self, printActions=True):
        """
        :param printActions: Imprime um log das ações principais feitas no jogo
        :type Float:
        """
        self.players = [] #array que contem todos os jogadores
        self.property = [] #array que contem todas as propriedades (bens)
        self.maxRound = 1000 #máximo de rounds permitidos
        self.playTurn = 0 #jogador que deve jogar
        self.rounds = 0 #contabiliza os rounds jogados
        self.printActions = printActions
        self.startMoney = 300 #dinheiro que o jogador inicia
        
        #Modelo retornado quando o jogo acabar
        self.finish = {
            'is_finish': False,
            'cause': 'winner',
            'winner': '',
            'turns': 0}

        #Tipos de jogadores e suas funções de compra (retorna quando comprar e quando não comprar)
        self.playerTypes = {
            'I': buy_fun_i, #Jogador impulsivo
            'E': buy_fun_e, #Jogador exigente
            'C': buy_fun_c, #Jogador cauteloso
            'A': buy_fun_a} #Jogador aleatório

    # idd:string que identifica o jogador. playerType: I-impulsivo,
    # E-exigente, C-cauteloso, A-aleatorio
    def add_player(self, playerType):
        '''Adiciona novo jogador ao jogo

        :param idd: id do jogador
        :type idd: integer
        :param playerType: Tipo do jogador I(impulsivo), E(exigente), C(cauteloso), A(aleatorio)
        :type playerType: character
        '''

        #define jogador
        player = {
            'buyFun': self.playerTypes[playerType],
            'money': self.startMoney,
            'properties': [],
            'position': 0,
            'loss': False,
            'player_type': playerType,
            'id':len(self.players)}
        
        self.players.append(player) #adiciona jogador a lista de players

    def add_property(self, price, rentValue):
        '''Cria nova propriedade

        :param price: Preço da propriedade
        :type price: float
        :param rentValue: Valor do aluguel
        :type rentValue: float
        '''
        
        self.property.append({'price': price,
                              'rent_value': rentValue,
                              'bought': False,
                              'owner': ''})

    def roll_dice(self):
        '''
        :return: Retorna numero entre 1-6
        :retype: integer
        '''
        return random.randint(1, 6)

    def roll_sequence_players(self):
        '''Define a sequencia aleatória que os jogadores irão jogar
        '''
        random.shuffle(self.players)

    def buy_property(self, property_, player):
        '''Player compra a propriedade
        '''
        if player['money'] >= property_['price']:
            property_['bought'] = True
            property_['owner'] = player
            if self.printActions:
                print(f'O jogador {player["id"]} tirou {rollNumber} e caiu na casa {player["position"]}'
                    ' comprando por {property_["price"]} a propriedade')
                    
        elif player['money'] < property_['price']:
            if self.printActions:
                print(f'O jogador {player["id"]} caiu na propriedade {player["position"]}'+
                    ' mas não comprou a propriedade por falta de dinheiro')
                    
        player['money'] -= property_['price']

    def pay_rent_property(self, property_, player):
        '''Player paga aluguel da propriedade
        '''
        player['money'] -= property_['rent_value']
        property_['owner']['money'] += property_['rent_value']

    def start_game(self):
        '''Executa ações para iniciar o jogo
        '''
        self.roll_sequence_players() #gerando a ordem aleatória dos jogadores
        
        #mudando o id de cada jogador de acordo com a posição
        for x in range(len(self.players)):
            self.players[x]['id'] = x

    def verify_win(self):
        '''Verifica se há um ganhador
        :return: Retorna True if houver ganhador
        :retype: bool
        '''
        if [x['loss'] for x in self.players].count(True) >= len(self.players) - 1: #Verifica se resta apenas um player que não perdeu
            if self.printActions:
                print('fim de jogo')
            if self.printActions:
                print(f'{self.rounds} rounds')
            winDic = {True: 'perdeu', False: 'Ganhou'}
            for x in self.players: #Loop para verificar qual jogador ganhou
                if self.printActions:
                    print(f'O jogador {x["id"]} {winDic[x["loss"]]}')
                if not x["loss"]:
                    self.winner = x #Define ganhador

            #Guarda os dados de como o jogo acabou
            self.finish = {
                'is_finish': True,
                'cause': 'winner',
                'winner': self.winner,
                'turns': self.rounds}

            return True

    def verify_timeout(self):
        '''Verifica se o jogo chegou ao lmites de rodadas
        '''
        if self.rounds >= self.maxRound:
            self.winner = max(self.players, key=lambda x: x['money']) #Define o ganhador o jogador com mais dinheiro
            
            #Guarda os dados de como o jogo acabou
            self.finish = { 
                'is_finish': True,
                'cause': 'timeout',
                'winner': self.winner,
                'turns': self.rounds}

    def play_turn(self):
        '''Processa uma rodada
        Processa todo o fluxo do jogo.
        Simula os dados rolando, a propriedade que cai, a escolha disponivel (comprar/não comprar) / pagar aluguel,
        e as consequencias com a escolha do player.
        Verifica se há ganhadores e calcula os proximos passos.
        '''

        self.listPlayers = [x for x in self.players if not x['loss']] #Exclui jogadores que já perdeu
        
        if self.finish['is_finish']: #verifica se há ganhador definido 
            return {'status': 'finish'} 

        self.verify_win() #verifica se há ganhador 
        self.verify_timeout() #verifica se atingiu maximo de rodadas

        if self.playTurn > len(self.listPlayers) - 1: #verifica se ultrapassou o ultimo jogador da lista de jogadores
            self.playTurn = 0 #seta o turno para o primeiro jogador

        playerTurn = self.listPlayers[self.playTurn] #Define qual jogador está jogando nessa rodada

        rollNumber = self.roll_dice() #rola os dados que define quantas casas o jogador vai andar 

        if rollNumber + playerTurn['position'] > len(self.property) - 1: #ferifica se o jogador deu a volta no tabuleiro
            playerTurn['position'] = rollNumber + \
                playerTurn['position'] - len(self.property) #define a posição do jogador contando da casa 0 do tabuleiro
            playerTurn['money'] += 100 #adiciona +100 de saldo para o jogador
            if self.printActions:
                print(f'O jogador {playerTurn["id"]} ganhou 100')
        else:
            #define a posição do jogador somando quanto saiu nos dados
            playerTurn['position'] = rollNumber + playerTurn['position'] 

        positionPlayer = playerTurn['position'] #pega a posição do jogador

        property_ = self.property[positionPlayer] #pega a propriedade que o jogador está

        if property_['bought']: #verifica se a propriedade está comprada
            self.pay_rent_property(property_, playerTurn) #jogador paga o aluguel da propriedade
            
            if self.printActions:
                print(f'O jogador {playerTurn["id"]} tirou {rollNumber} e caiu'+
                      'na casa {positionPlayer} pagando {property_["rent_value"]} de aluguel')

        else: #se a propriedade não estiver comprada

            #verifica se o jogador quer ou não comprar a casa, a partir de sua função de compra
            buyDecision = playerTurn['buyFun'](property_, playerTurn)

            #se o jogador quiser comprar e tiver dinheiro suficiente
            if buyDecision:
                self.buy_property(property_, playerTurn) #jogador compra a propriedade
                    
            elif not buyDecision:
                if self.printActions:
                    print(f'O jogador {playerTurn["id"]} tirou {rollNumber} e caiu na casa {positionPlayer} '+
                        'mas não quis comprar')

        if playerTurn['money'] < 0: #Verifica seo jogador perdeu
            if self.printActions:
                print(f'O jogador {playerTurn["id"]} perdeu. Saldo:{playerTurn["money"]}')
                
            for x in property_:
                if property_['owner'] == playerTurn:
                    property_['owner'] = ''
                    property_['bought'] = False

            playerTurn['loss'] = True

        self.playTurn += 1

        if self.listPlayers[-1] == playerTurn: #Verifica se finalizou uma rodada
            self.rounds += 1                   #Adiciona 1 à variavel de rodadas
        
        return {'status': 'in_progress'}


class GenerateSimulationSession:
    """Classe gera as simulações, gerencia as rodadas e
    relaciona os dados de cada sessão
    """
    def __init__(self, sizeSimulation, valuesRange=(50, 150), rangeRentPercent=(0.1, 0.5)):
        """
        :param sizeRound: Quantidade de simulações que serão executadas
        :type sizeRound: int
        :param maxTurn: Quantidade máxima 
        :type maxTurn: int
        :param valuesRange: Variação dos valores do imovel
        :type valuesRange: tuple
        :param range_rent_percent: Variação do aluguel de 0 a 1
        :type range_rent_percent: tuple
        """
        self.sizeSimulation = sizeSimulation
        self.data = []
        self.valuesRange = valuesRange
        self.rangeRentPercent = rangeRentPercent
        

    def start_simulation(self):
        for x in range(self.sizeSimulation): #Loop da quantidade de simulações
            self.game = BancoImobiliario(printActions=False) #Cria uma instancia da classe BancoImobiliario
            self.game.add_player('I') #adiciona jogadordo tipo impulsivo
            self.game.add_player('E') #adiciona jogadordo tipo exigente
            self.game.add_player('C') #adiciona jogadordo tipo cauteloso
            self.game.add_player('A') #adiciona jogadordo tipo aleatório

            #adiciona 20 propriedades ao jogo com valores de compra e aluguel aleatórios 
            for x in range(20):
                price = random.randint(self.valuesRange[0], self.valuesRange[1]) #valor de compra
                rent = random.uniform(
                    self.rangeRentPercent[0],
                    self.rangeRentPercent[1]) * price #valor de aluguel
                self.game.add_property(price, rent) #adiciona propriedade


            #Inicia o jogo
            while True:
                turn = self.game.play_turn() #processa uma jogada
                if turn['status'] == 'finish': #verifica se o jogo acabou
                    self.data.append(self.game.finish) #adicina informações do fim de jogo a varivel data
                    break

        #Quando todas as simulações acabam o calculo dos dados é feito
        self.setsTimeOut = [x['cause'] for x in self.data].count('timeout') #calcula quantas partidas tiveram timeout
        print(f'Partidas com timeout {self.setsTimeOut}')
        
        self.turnsList = [x['turns'] for x in self.data] #cria array com quantidade de turnos de cada partida
        self.turnsMean = round(sum(self.turnsList) / len(self.turnsList)) #calcula quantos turnos em média demora uma partida
        print(f'As partidas demoram em média {self.turnsMean} rodadas')

        types = {'I':'impulsivo','E':'exigente','C':'cauteloso','A':'aleatório'}
        self.winnerPlayerType = [x['winner']['player_type'] for x in self.data] #cria array com tipo de jogador
                                                                                #vitorioso de cada simulação
        #calcula a porcentagem de vitórias por comportamento dos jogadores
        self.winnerPlayers = {types[x]: str(round(self.winnerPlayerType.count( 
            x)/self.sizeSimulation*100))+'%' for x in self.game.playerTypes.keys()}
        print(f'Porcentagem de vitórias por comportamento dos jogadores:')
        print(self.winnerPlayers)
        
        self.BigPlayerWinner = max(self.winnerPlayers) #Verifica qual o comportamento que mais vence.
        print(f'Comportamento que mais vence: {self.BigPlayerWinner}')


#gerando simulação com 300 jogos, valores dos imoveis de 50 a 150.Valor do aluguel de 10% a 50% do valor do imovel
aa = GenerateSimulationSession(sizeSimulation=300, valuesRange=(50, 150), rangeRentPercent=(0.1, 0.5))
aa.start_simulation()
