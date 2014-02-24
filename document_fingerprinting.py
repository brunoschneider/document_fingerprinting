#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import division
import nltk
import glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import collections
from ignore import lista_ignorar # uma lista de exceções com tokens que não se deseja processar está definida no arquivo ignore.py
from metrics import simpsons_index, lexical_diversity, hapax_legomena

# Essa função recebe um caminho no disco (local) onde estão armazenados todos os arquivos.. 
# ..a serem processados e retorna uma lista com o caminho específico de cada um dos arquivos contidos na pasta 
def caminhotxt(path):
    archives_list = []
    saida = []
    for fil in glob.glob(path):
        saida.append(fil)
    for x in sorted(saida):
        archives_list.append(x)
    return archives_list

# Essa função recebe a lista de caminhos gerada pela função anterior, lê os textos (em formto txt) e faz a tokenização dos mesmos,
# aplica uma determinada metrica de diversidade léxica dentre as 3 disponíveis (a partir do parâmetro 'metrica' que deve ser escolhido na chamada da função) e..
# ..gera como saída um dicionário onde cada chave é o caminho de cada um dos arquivos lidos e os valor associado a essa chave é uma lista..
#.. de números obtida a partir do processamento dos textos em fragmentos de 'n' tokens (onde 'n' também é parâmetro da função) utilizando a métrica escolhida. Cada elemento numérico da lista correponde à aplicação da métrica sobre os sucessivos fragmentos de tamanho 'n' tokens ao longo de cada txt lido.

def letxt_aplicametrica(archives_list, n, metrica):
    ignorar = lista_ignorar
    dicionario = {}
    var = n

    for x in range(len(archives_list)):
        f = open(archives_list[x])
        raw = f.read()
        f.close()
        tokens = nltk.wordpunct_tokenize(raw.decode('utf8'))
        lista = []
        for w in tokens:
            if w not in ignorar:
                lista.append(w.encode('utf-8'))
        a = 0
        
        # na variável abaixo está definido que o nível de sobreposição entre os fragmentos de tokens a serem processados será de..
        # .. 90 por cento, pois apenas 0.1 (10 por cento) de tokens novos serão incorporados a cada novo fragmento
        c = int(0.1 * n)
        if c == 0:
            c = 1

        tam = len(lista)
        lista2 = []
        
        while n <= tam:
            fragmento = lista[a:n]
            lista2.append(metrica(fragmento))
            a = a + c
            n = n + c
        n = var
        final = lista[a:]
        
        lista2.append(metrica(final))
        
        dicionario[archives_list[x]] = lista2
    return dicionario
    
# início da função de visualização que recebe como entrada o dicionário gerado pela função anterior, o tamanho do plot (xsize e ysize) e ainda o título do gráfico a ser plotado
def visualiza(dicionario, xsize, ysize, titulo):
    # inicializando a figura e gerando a barra de cor lateral
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg = 'black')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    PuOr = plt.get_cmap('PuOr') # escolha da escala de cor que será utilizada dentre as já disponíveis no matplotlib
    cmaplist = [PuOr(i) for i in range(PuOr.N)]
    cx = ax.imshow(cmaplist,interpolation='nearest', cmap = 'PuOr', visible = None)
    cbar = fig.colorbar(cx)
    x = -xsize + 30
    y = ysize -50
    ax.set_title(titulo) # impressão do título do gráfico na saída a ser visualizada tendo como entrada o parâmetro 'título' da função

    # calculando o valor maximo do dicionário para a normalizacao dos valores
    m = max(sum(dicionario.values(), []))

    # iterando pelos dicionarios 
    od = collections.OrderedDict(sorted(dicionario.items()))
    num_col = 0
    num_lin = 0
    
    # a altura de cada bloco dos fingeprints está definida como 8 quadrados por padrão 
    # (a largura varia em função do tamanho do texto)
    for k, v in od.iteritems():
        s = len(v)
        if (s % 8) == 0:
            num_col = (s / 8)
        if (s % 8) != 0:
            num_col = int(s/8) + 1
        if num_col > 1:
            num_lin = 8
        if num_col == 1:
            num_lin = s
        
        # gerando o array de uma chave do dicionario
        b = np.zeros((num_lin, num_col))
        n = 0
        for i in range(int(num_lin)):
            for j in range(int(num_col)):
                if n <= (s - 1):
                    b[i][j] = v[n]
                    n = n + 1
                else:
                    b[i][j] = 0
                    
        # plotando o array de uma chave do dicionario
        
        tam_quad = 15 # essa variavel define o tamanho em pixels de cada quadrado que será plotado
        xmax = xsize - 25
        marg = 25
        x_acumul_array = (num_col * tam_quad)
        if (x + x_acumul_array + marg) > xmax:
            y = y - ((8 * tam_quad) + marg)
            x = -xsize + 25
        for i in range(int(num_lin)):
            for j in range(int(num_col)):
                if b[i][j] == 0:
                    rect = matplotlib.patches.Rectangle((x, y), tam_quad, tam_quad, color = 'Black')
                    ax.add_patch(rect)
                    x = x + tam_quad
                else:    
                    rect = matplotlib.patches.Rectangle((x, y), tam_quad, tam_quad, color = PuOr(b[i][j]/m))
                    ax.add_patch(rect)
                    x = x + tam_quad
            x = x - (num_col * tam_quad)
            y = y - tam_quad
        x = x + (num_col * tam_quad) + marg
        y = y + (num_lin * tam_quad)

    # utilização dos parâmetros xsize e ysize da função para a geração do plot
    plt.xlim([-xsize, xsize])
    plt.ylim([-ysize, ysize])
    plt.show()

# MELHORIAS PREVISTAS 
# organizar as funções dentro de classes para melhor controle do script e da geração dos gráficos
# melhorar a lista de exceção de tokens para exclusão do processamento de linguagem; a lista atual é absolutamente provisória

#testando
teste = caminhotxt('data/*.txt')
teste2 = letxt_aplicametrica(teste, 1000, lexical_diversity)
v = visualiza(teste2, 400, 600, u'Constituição brasileira de 1988 - Diversidade léxica')
