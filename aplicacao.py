#Código teste OTA

version = [0, 1, 0]
"""
Classes/Objetos que servem para criar uma rede neural.
É flexível na criação de redes.
Existem duas classes, o Neuron e a Network. Uma Network é composta por Neuron's connectados.
"""

#from neural_functions_c import activation_C

#O neurônio pode servir para criar manualmente qualquer tipo de arquitetura para rede neural
class Neuron: #Pode ser tanto o input layer quanto o proprio neurônio, a função de ativação e o output.
    """
    Cria um objeto que pode ser tanto um input quanto um neurônio quanto um output, você não precissa indentificar o que ele é.
    """
    __slots__ = ("value", "connections", "returns", "weights", "factor_correction", "learn", "activation_function", "derivative_function")
    def __init__(self, learn = 0.05, activation_function = "sigmoid", derivative_function = None):
        self.value = None #Valor principal
        self.connections = None #Conecções
        self.returns = None #Conecções de retorno
        self.weights = None #Pesos
        self.factor_correction = None #Fator de correção
        self.learn = learn
        self.activation_function = activation_function.lower()
        self.derivative_function = derivative_function
        
    def connect(self, connections):
        """
        connecta um objeto a outros, o unico tipo de objeto que não dever ser connectado é o output.
        """
        
        from random import random
        
        if type(connections) != list: #Se você não passar uma lista
            connections = [connections]

        if self.connections == None:
            self.connections = connections #Liga as conecções
        else:
            self.connections.extend(connections)
        
        for nexts in self.connections: #Liga os retornos
            
            if nexts.returns == None:
                nexts.returns = []
            nexts.returns.append(self)

            if self.weights == None:
                self.weights = []
            self.weights.append(random()*2-1)

    #Uma função que tem no ponto de entrada o Input ou um neuronio e no de saida um neuronio:
    def distribute(self):
        """
        Faz a distribuição dos pesos entre os objetos.
        """
        if len(self.connections) == len(self.weights):
            for k in range(len(self.connections)):
                if self.connections[k].value == None:
                    self.connections[k].value = 0 #Agora a conecção pode receber um valor
            for i in range(len(self.connections)):
                self.connections[i].value += self.weights[i] * self.value

        else:
            from random import random
            print(f"Yours vectors connections and weights are diferent lens, {len(self.connections)} and {len(self.weights)}")
            self.weights = [random() - 0.5 for i in range(len(self.connections))]
            pass

    #Exclusivo do Input:
    def input(self, value):
        self.value

    #Função de ativação:
    def activation(self): #Depois tem que colocar o ativation = False
        """
        Sigmoide, serve para a ativação do objeto.
        """
        if self.activation_function == "sigmoid":
            try:
                e = float(2.7182)
                self.value = 1/(1 + e ** (-1*self.value))
            except OverflowError:
                pass
            except TypeError:
                self.value = 0
        elif self.activation_function == "relu":
            try:
                self.value = max(0, self.value)
            except OverflowError:
                pass
        else:
            self.value = self.activation_function(self.value)
        

    def correction(self,value):
        """
        Descobre o fator de correção.
        """
        if self.returns != None:
            for neurons in self.returns: #Output
                if neurons.returns != None: #Se ele tiver retornos e conecções (conecções ele já tem obrigatoriamente)
                    if self.activation_function == "sigmoid":
                        initial_factor = (1-neurons.value)*neurons.value
                    elif self.activation_function == "relu":
                        if neurons.value > 0:
                            initial_factor = 1
                        else:
                            initial_factor = 0
                    else:
                        self.derivative_function(neurons.value)
                        
                    if neurons.factor_correction == None:
                        neurons.factor_correction = 0
                                            
                    for i in range(len(neurons.connections)):                        
                        neurons.factor_correction += neurons.weights[i] * neurons.connections[i].factor_correction
                    neurons.factor_correction *= initial_factor

    def change_weights(self): #Muda os pesos de acordo com o fator de correção
        """
        Troca os pesos de acordo com o fator de correção.
        """
        for i in range(len(self.connections)):
            self.weights[i] -= (self.value * self.connections[i].factor_correction) * self.learn #fator de aprendizado = 0.01

    def prints(self):
        """
        Printa as propriedades do objeto.
        """
        print("Value " + str(self.value) + "\n" +
            "connections " + str(self.connections) + "\n" +
            "Returns " + str(self.returns) + "\n" +
            "Weights " + str(self.weights) + "\n" +
            "Corretion " + str(self.factor_correction))
    
#Arquitetura simples de rede neural, input -> neuronios -> output
class Network:
    """
    Após definir uma lista de listas de neuronios, você pode criar uma rede, ela será responsável pelo controle geral das conecções.
    """
    __slots__ = ("network", "value", "print_", "one_hot")
    def __init__(self, network = None, value = None, one_hot = False):
        #network é um array onde cada vetor é uma camada            
        if network != None and type(network) == list:
            self.network = network
            self.fill()       
        else:
            self.network = None
            print("You need pass a list of layers")
            
        self.print_ = True
        self.value = value
        self.one_hot = one_hot

    def properties(self):
        """
        Diz algumas propriedades da rede.
        """
        if self.network != None:
            print("There are",len(self.network[0]),"inputs,",len(self.network[-1]),"outputs and",len(self.network)-2,"layers")
        else:
            print("You haven't set the network yet")

    def size(self):
        from sys import getsizeof as sf
        
        total_size = 0
        total_size += sf(self) + sf(self.value) + sf(self.one_hot) + sf(self.print_)
        
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                total_size += sf(self.network[i][j]) + sf(self.network[i][j].weights) + sf(self.network[i][j].weights) \
                              + sf(self.network[i][j].value) + sf(self.network[i][j].connections) + sf(self.network[i][j].returns) \
                              + sf(self.network[i][j].factor_correction) + sf(self.network[i][j].learn) + sf(self.network[i][j].activation_function) \
                              + sf(self.network[i][j].derivative_function)

        if total_size < 1024 * 10:
            l = "b"
            size_final = total_size
        elif total_size < (1024 ** 2)/10:
            l = "kb"
            size_final = total_size/1024
        else:
            l = "mb"
            size_final = total_size/1024**2
                
        print(f"Neural network size is approximately: {size_final}{l}")

    def fill(self): #Preenche com o valor 1 os neuronios de viés
        """
        Completa os inputs ou neuronios de viés com 1.
        """
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                if self.network[i][j].value == None and self.network[i][j].returns == None:
                    self.network[i][j].value = 1 #Se torna um neuronio de viés
    
    def run(self):
        """
        Faz um caminho de ida e volta na rede, corrigindo seus pesos com o BackPropagation.
        """
        self.simple_run()

        if self.value == None: #Se
            print("There is no y defined to BackPropagations")
            return

        for i in range(len(self.network[-1])): #Ultima camada
            if self.network[-1][i].connections == None: #Se for um output
                self.network[-1][i].factor_correction = self.network[-1][i].value - self.value[i]

        for i in range(len(self.network[-1])): #BackPropagation da ultima camada
            self.network[-1][i].correction(self.value[i])

        for i in range(len(self.network)-2, 1, -1): #BackPropagation daS camadas restantes
            for j in range(len(self.network[i])):
                    self.network[i][j].correction(self.value)

        for i in range(len(self.network)-1): #Correção dos pesos
            for j in range(len(self.network[i])):
                self.network[i][j].change_weights()         

    def simple_run(self):
        """
        Faz um caminho apenas de ida na rede.
        """
        max_ = len(self.network) - 1 #Onde o output fica
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                if i != 0 and j != 0 or i == max_: #No imput ele não precisa fazer a ativação nem nos viéses j = 0 e i > 0
                    self.network[i][j].activation()
                if i != max_: #No output ele não faz a distribuição
                    self.network[i][j].distribute()

    def exist_nan(self):
        """
        Se por algum motivo existe um valor infinito ou um 'not a number' na rede ele retorna True.
        """
        from random import random
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                if str(self.network[i][j].value) == "nan" or str(self.network[i][j].value).find("inf") > -1:
                    self.network[i][j].value = random()*2 - 1
                    return True
                if str(self.network[i][j].factor_correction) == "nan" or str(self.network[i][j].factor_correction).find("inf") > -1:
                    self.network[i][j].factor_correction = random()*2 - 1
                    return True

                try:
                    for k in range(len(self.network[i][j].weights)):
                        if str(self.network[i][j].weights[k]) == "nan" or str(self.network[i][j].weights[k]).find("inf") > -1:
                            self.network[i][j].weights[k] = random()*2 - 1
                            return True
                except TypeError:
                    pass
        return False

    def train(self, inputs, values, times): #Treina a rede
        """
        Treina a rede.
        """
        if len(inputs[0]) != len(self.network[0]):
            print("Your inputs have to be of size", len(self.network[0]))
            return

        if len(inputs) != len(values):
            print("Your list input have to be of size", len(values), f"you have {len(inputs)} and {len(values)}")
            return

        cont = True
        for t in range(times):
            try:
                if t % int(times/20) == 0:
                    print(str(t/times * 100 + 5)[:4] + "%")
            except:
                pass
            if cont:
                for i in range(len(inputs)): #Coloca os inputs novos para treino
                    for j in range(len(self.network[0])):
                        self.network[0][j].value = inputs[i][j]
                            
                    self.value = values[i]
                    self.run()

            if not self.exist_nan():
                backup = Network(self.network)
            else:
                try:
                    self = backup
                except:
                    pass
                print("Truncation or numeric representation error\n(if this happens often the problem may be in the network design)")
                return self.train(inputs, values, int(times*.25))

    def answer(self, inputs):
        """
        Diz quais são os outputs.
        """
        if type(inputs) != tuple and type(inputs) != list:
            print("You must pass a list of inputs")
            return

        if len(inputs) != len(self.network[0]):
            print("Your inputs have to be of size", len(self.network[0]))
            return
        
        for j in range(len(self.network[0])): #Não considera valores fixos
            self.network[0][j].value = inputs[j]
        self.simple_run()

        if type(self.one_hot) == bool:
            if self.print_ and not self.one_hot:
                print(inputs)
                for i in range(len(self.network[-1])):
                    print("y(" + str(i) + ") = " + str(self.network[-1][i].value))
                print("")

            if self.print_ and self.one_hot:
                print(inputs)
                resps = []
                for i in range(len(self.network[-1])):
                    resps.append(self.network[-1][i].value)
                resps_new = [0 for i in range(len(resps))]
                resps_new[resps.index(max(resps))] = 1
                for i in resps_new:
                    print("y(" + str(i) + ") = " + str(i))
                print("")
        else:
            if self.print_:
                print(inputs)
                resps = [0 for i in range(len(self.network[-1]))]
                for i in range(len(self.network[-1])):
                    if self.network[-1][i].value >= self.one_hot:
                        resps[i] = 1
                for i in resps:
                    print("y(" + str(i) + ") = " + str(i))
                print("")
        
    def view(self):
        """
        Ajuda a visualizar a rede.
        """
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                print("Layer["+str(i)+"] neuron["+str(j)+"] = "+str(self.network[i][j].value)+" | w = "+" | c = "+str(self.network[i][j].factor_correction)+str(self.network[i][j].weights))

    def export_(self, name = "neural_network"): #Salva os pesos de neuronios
        """
        Exporta os pesos da rede.
        """
        if name.find(".json") == -1:
            name += ".json"
        
        import json
        list_neurons = []
        
        for i in range(len(self.network)):
            temp_list = []
            for j in range(len(self.network[i])):
                temp_list.append(self.network[i][j].weights)
            list_neurons.append(temp_list)
            
        arq = json.dumps(list_neurons, sort_keys = False, indent = -1)
        with open(name, "w") as file:
            file.write(arq)
            
        print("Save json with name",name)

    def export_design(self, name = "design_neural_network"): #Salva todo design da rede
        """
        Exporta tanto a estrutura das redes quanto seus pesos.
        """
        if name.find(".json") == -1:
            name += ".json"
        
        import json

        list_structure = []
        #Pega a estrutura:
        for i in range(len(self.network) - 1): #Para cada layer
            tmp_st = []
            for j in range(len(self.network[i])): #Para cada objeto do layes
                tmp_st2 = []
                for k in range(len(self.network[i][j].connections)): #Para cada conecção
                    #Ache o equivalente nos layers posteriores
                    for n in range(i, len(self.network)): #Para cada layer posterior
                        for m in range(len(self.network[n])): #Para cada objeto do layes
                            if self.network[i][j].connections[k] ==  self.network[n][m]:
                                tmp_st2.append((n,m))
                tmp_st.append(tmp_st2)
            list_structure.append(tmp_st)    

        #Pega a memória:
        list_neurons = []
        for i in range(len(self.network)):
            temp_list = []
            for j in range(len(self.network[i])):
                temp_list.append(self.network[i][j].weights)
            list_neurons.append(temp_list)
            
                
        arq = json.dumps((list_neurons,list_structure))
        with open(name, "w") as file:
            file.write(arq)
            
        print("Save json with name",name)

    def import_(self, name = "neural_network"): #Importa os pesos dos neuronios
        """
        Importa pesos externos para sua rede.
        """
        if name.find(".json") == -1:
            name += ".json"

        import json

        with open(name, "r") as openfile:
            import_n = json.load(openfile)

        print(import_n)
        try:
            if len(import_n) != len(self.network):
                print("Use a import with same len of you neural network!")
                return
        except TypeError:
            print("The structure of the neural network is not clear!")
            return

        for i in range(len(import_n)-1):
            for j in range(len(import_n[i])):
                self.network[i][j].weights = import_n[i][j]

        self.fill()

    def import_design(self, name = "design_neural_network"): #Importa o design dos neuronios
        """
        Importa a estrutura completa da rede interpretando pesos e conecções.
        """
        if name.find(".json") == -1:
            name += ".json"

        import json

        with open(name, "r") as openfile:
            import_n = json.load(openfile)

        #Cria os neuronios:
        temp_nrl = []
        for i in range(len(import_n[0])):
            temp_nrl2 = []
            for j in range(len(import_n[0][i])):
                temp_nrl2.append(Neuron())
            temp_nrl.append(temp_nrl2)

        self.network = temp_nrl

        #Cria as conecções:
        for i in range(len(self.network)-1):
            for j in range(len(self.network[i])):
                for k in range(len(import_n[1][i][j])):                  
                    self.network[i][j].connect(self.network[import_n[1][i][j][k][0]][import_n[1][i][j][k][1]])

        #Adiciona os pesos aos neuronios criados:
        for i in range(len(import_n[0])-1):
            for j in range(len(import_n[0][i])):
                self.network[i][j].weights = import_n[0][i][j]

        from random import random

        for i in range(len(self.network)-1):
            for j in range(len(self.network[i])):
                if len(self.network[i][j].connections) != len(self.network[i][j].weights):
                    self.network[i][j].weights = [random() for i in range(len(self.network[i][j].connections))]

        self.fill()
    
    def __repr__(self):
        """
        Método especial.
        """
        k = ""
        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                k += "Layer["+str(i)+"] neuron["+str(j)+"] = "+str(self.network[i][j].value)[:5]+" | w = "+str(self.network[i][j].weights)+" | c = "+str(self.network[i][j].factor_correction)[:7]+"\n"
        self.size()
        return k

    def __invert__(self): # ~rede por exemplo
        """
        Método especial que roda a rede uma vez. ~rede por exemplo.
        """
        self.run()

    def __rshift__(self, times): # rede >> 2 por exemplo
        """
        Método especial que roda a rede um determinado numero de vezes. rede >> 2 por exemplo.
        """
        for i in range(times):
            self.run()

    def __eq__(self, inputs): #rede == [0,0] por exemplo
        """
        Método especial que aceita entradas. rede == [0,0] por exemplo.
        """

        self.answer(inputs)
        resp = []
##        for i in range(10000):
##            try:
##                resp.append(self.network[-1][i].value)
##            except:
##                return resp

        if type(self.one_hot) == bool:
            if self.print_ and not self.one_hot:
                for i in range(len(self.network[-1])):
                    resp.append(self.network[-1][i].value)

            if self.print_ and self.one_hot:
                for i in range(len(self.network[-1])):
                    resp.append(self.network[-1][i].value)
                resps_new = [0 for i in range(len(resp))]
                resps_new[resp.index(max(resp))] = 1
                resp = resps_new
        else:
            if self.print_:
                resp = [0 for i in range(len(self.network[-1]))]
                for i in range(len(self.network[-1])):
                    if self.network[-1][i].value >= self.one_hot:
                        resp[i] = 1

        return resp

    def __getitem__(self, index): #rede[0] por exemplo
        """
        Método especial que retorna um layer. rede[0] por exemplo.
        """
        return self.network[index]


def mlp(design:list, bias:bool = True, one_hot = False, **args):
    network = []
    for i in range(len(design)):
        temp_network = []
        for j in range(design[i]):
            globals()[f"n{i}_{j}"] = Neuron(**args)
            temp_network.append(globals()[f"n{i}_{j}"])
        network.append(temp_network)

    for i in range(len(design) - 1):
        for j in range(design[i]):
            temp = []
            if i+2 != len(design):
                for k in range(bias, design[i+1], 1):
                    temp.append(globals()[f"n{i + 1}_{k}"])
            else:
                for k in range(0, design[i+1], 1):
                    temp.append(globals()[f"n{i + 1}_{k}"])

            globals()[f"n{i}_{j}"].connect(temp)

    return Network(network, one_hot = one_hot)

def cnn(input_image:list = [16, 16], design:list = [{"stride":2, "lenth":3, "amount":1}], one_hot = False, **args):
    temporari = {}

    temporari[0] = [[Neuron(**args) for i in range(input_image[0])] for j in range(input_image[1])]
    
    c = 1
    for dsg in design:
        if not "fc" in dsg.keys():
            a = int((input_image[0] - dsg["lenth"])/dsg["stride"] + 1)
            b = int((input_image[1] - dsg["lenth"])/dsg["stride"] + 1)
            temporari[c] = [[Neuron(**args) for i in range(a)] for j in range(b)]
            for i in range(len(temporari[c - 1])):
                for j in range(len(temporari[c - 1][0])):
                    
                    temporari[c-1][i][j].connect(temporari[c][int(i/dsg["lenth"])][int(j/dsg["lenth"])])
            print((i, j), "to", (int(i/dsg["lenth"]), int(j/dsg["lenth"])))
        else:
            temporari[c] = [Neuron(**args) for i in range(dsg["fc"])]
            for i in range(len(temporari[c - 1])):
                for j in range(len(temporari[c - 1][0])):
                    for k in range(len(temporari[c])):
                        temporari[c-1][i][j].connect(temporari[c][k])
        c += 1

    final_network = []
    for k in temporari.keys():
        temp = []
        for l in temporari[k]:
            try:
                temp.extend(l)
            except:
                temp.append(l)
        final_network.append(temp)

    
    return Network(final_network, one_hot = one_hot)
        
#--------------------------------------------------------------------------------

if __name__ == "__main__":
    from time import time
    
##    #Inputs
##    i1 = Neuron()
##    i1.value = 1
##
##    i2 = Neuron()
##    i2.value = 1
##
##    i3 = Neuron()
##    i3.value = 1
##
##    n11 = Neuron()
##    n12 = Neuron()
##    n13 = Neuron()    
##
##    n21 = Neuron()
##    n22 = Neuron()
##    n23 = Neuron()
##
##    o1 = Neuron()
##    o2 = Neuron()
##
##    #Conecções
##    i1.connect([n12, n13])
##    i2.connect([n12, n13])
##    i3.connect([n12, n13])
##
##    n11.connect([n22, n23])
##    n12.connect([n22, n23])
##    n13.connect([n22, n23])
##
##    n21.connect([o1,o2])
##    n22.connect([o1,o2])
##    n23.connect([o1,o2])
##
##    rede = Network([[i1,i2,i3],
##                    [n11,n12,n13],
##                    [n21,n22,n23],
##                    [o1,o2]])
##
##    t1 = time()
##    rede.train([[1,0,0],[1,0,1],[1,1,0],[1,1,1]],[[1,0],[0,1],[1,1],[0,0]],40000)
##    t2 = time()
##    print(t2-t1,"\n")      
##
##    rede == [1,0,0]
##    rede == [1,0,1]
##    rede == [1,1,0]
##    rede == [1,1,1]

    #rede = mlp([3,8,8,2], bias = True, activation_function = "sigmoid", learn = 0.1, one_hot = False)

    rede = mlp([16*16,8,8,10], bias = True, learn = 0.3)
##    print(rede)
    
##    rede.train([[1,0,0],[1,0,1],[1,1,0],[1,1,1]],[[1,0],[0,1],[1,1],[0,0]], 2000)
##    
##    rede == [1,0,0]
##    rede == [1,0,1]
##    a = rede == [1,1,0]
##    rede == [1,1,1]

##    rede = cnn([16, 16], design = [{"stride":2, "lenth":3, "amount":1},
##                                   {"fc":10}], learn = 0.3)

    from PIL import Image
    import os
    pasta_imagens = 'C:/Users/Usuario/Desktop/digitos'
    lista_de_imagens = []
    for arquivo in os.listdir(pasta_imagens):
        if arquivo.endswith(".png"):
            caminho_completo = os.path.join(pasta_imagens, arquivo)
            try:
                imagem = Image.open(caminho_completo).convert("L")
                dados_imagem = list(imagem.getdata())
                lista_de_imagens.append(dados_imagem)
            except Exception as e:
                print(f"Erro ao processar {caminho_completo}: {str(e)}")

    for i in range(len(lista_de_imagens)):
        for j in range(len(lista_de_imagens[i])):
            lista_de_imagens[i][j] /= 255

    resp = [
            *[[0,1,0,0,0,0,0,0,0,0]] * 3,
            *[[0,0,1,0,0,0,0,0,0,0]] * 3,
            *[[0,0,0,1,0,0,0,0,0,0]] * 3,
            *[[0,0,0,0,1,0,0,0,0,0]] * 3,
            *[[0,0,0,0,0,1,0,0,0,0]] * 3,
            *[[0,0,0,0,0,0,1,0,0,0]] * 3,
            *[[0,0,0,0,0,0,0,1,0,0]] * 3,
            *[[0,0,0,0,0,0,0,0,1,0]] * 3,
            *[[0,0,0,0,0,0,0,0,0,1]] * 3,]

    rede.train(lista_de_imagens, resp, 100)

