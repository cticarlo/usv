"""
Definição do dicionário de telemetria. Colocado em script separado para melhor organização
O dicionário se chama tl (mnemônico para telemetria), e segue o padrão de payloads para consumo
pelo Thingsboard. O padrão divide o dado de telemetria em duas partes:
   - ts : timestamp -> informação de data e hora em milissegundos (referência de tempo)
   - values: dados a registrar -> é um dicionário, onde cada chave representa uma grandeza a monitorar

Não é recomendável hierarquizar mais o dicionário de grandezas e,
por isso, optou-se por criar um padrão de chaves, onde a primeira parte define o sensor
e a segunda parte descreve a variável medida. Até o momento, o que se tem:

   - gps_sat: número de satélites com trava no gps (inteiro);
   - gps_lat: latitude em graus decimais (real);
   - gps_lon: longitude em graus decimais (real);
   - gps_vel: velocidade em km/h
   - gps_cur: curso em graus decimais (0-359.9 - real);
   - gps_alt: altitude em m (real);
   - mcu_v: tensão medida no microcontrolador (real);
   - mcu_st: estado do microcontrolador (inteiro a decodificar);
   - bat_v: tensão medida na saída da bateria em V (real);
   - bat_i: corrente medida ao sair da bateria em A (real);
"""

tl = {"ts": 0,
      "values": {
        "gps_sat": None,
        "gps_lat": None,
        "gps_lon": None,
        "gps_vel": None,
        "gps_cur": None,
        "gps_alt": None,
        "mcu_v": None,
        "mcu_st": None,
        "bat_v": None,
        "bat_i": None}}
