import pandas




def save(G,adress=""):
    V_attributes={'index':[],'coordinates':[],'id':[],'gare_name':[],'color':[],'is_a_station':[],'index_edges_list':[]}
    E_attributes={'index':[],'index_linked[0]':[],'index_linked[1]':[],'given_cost':[],'color':[],'id':[],'connection_with_displayable':[]}
    devE_attributes={'connection_with_displayable':[],'connection_table_edge_and_diplayable_edge':[]}
    for i in range(G.number_of_vertices):
        v=G[i]
        assert(v.index==i),"Risque de déreglemment de la table"
        V_attributes['index'] .append(v.index)
        V_attributes['coordinates'] .append( v.coordinates)
        V_attributes['id'] .append(v.id)
        V_attributes['gare_name'].append(v.gare_name)
        V_attributes['color'].append(v.color)
        V_attributes['is_a_station'].append(v.is_a_station)
        V_attributes['index_edges_list'].append([e.index for e in v.edges_list])
    for i in range(len(G.list_of_edges)):
        e=G.list_of_edges[i]
        assert(e.index==i),"Risque de déreglemment de la table"
        E_attributes['index'].append(e.index)
        E_attributes['index_linked[0]'].append(e.linked[0].index)
        E_attributes['index_linked[1]'].append(e.linked[1].index)
        E_attributes['given_cost'].append(e.given_cost())
        E_attributes['color'].append(e.color)
        E_attributes['id'].append(e.id)
        E_attributes['connection_with_displayable'].append(e.connection_with_displayable)

    assert(G.number_of_edges==len(G.connection_table_edge_and_diplayable_edge)),"Risque de déreglemment de la table"
    devE_attributes['connection_with_displayable']=[i for i in range(G.number_of_edges)]
    devE_attributes['connection_table_edge_and_diplayable_edge']=G.connection_table_edge_and_diplayable_edge

    PandaV = pandas.DataFrame(V_attributes)
    PandaE = pandas.DataFrame(E_attributes)
    PandadevE = pandas.DataFrame(devE_attributes)

    print(PandaV .dtypes)
    print(PandaE. dtypes)
    print(PandadevE. dtypes)

    PandaV.to_pickle(adress+'datas/PandaV.pkl')
    PandaE.to_pickle(adress+'datas/PandaE.pkl')
    PandadevE.to_pickle(adress+'datas/PandadevE.pkl')
    #PandaV.to_excel(adress+'datas/PandaV.xlsx')
    #PandaE.to_excel(adress+'datas/PandaE.xlsx')
    #PandadevE.to_excel(adress+'datas/PandadevE.xlsx')
