import gc
from machine import UART, RTC # type: ignore
from light_nmea import LightNMEA, CST_MASK_GPS


class GPS(object):
    '''
    Define uma classe para gerenciar o uso do GPS e atualização dos dados do dicionário de telemetria
    Voltado para o GPS NEOv6m, com comunicação serial
    '''
    def __init__(self, tl, uart=1, bps=9600, tx=17, rx=18):
        self.ser = UART(uart, baudrate=bps, tx=tx, rx=rx)
        self.parser = LightNMEA(trust_gga_fix=True) # Confia no fix de msgs GGA
        self.parser.set_cst_filter(CST_MASK_GPS) # Apenas mensagens GPS
        self.tl = tl
        self.gcc = 0
        self.nmea = b""


    def atualizar(self):
        '''
        Verifica se há dados na serial, e em caso de haver, atualiza a telemetria
        Retorna True, se houve atualização, ou False, do contrário
        '''
        try:
            r = False
            if self.ser.any(): # Há algo no buffer de entrada
                self.nmea = self.ser.readline()
                if self.nmea and len(self.nmea) > 10: # O conteúdo pode ser válido
                    if self.parser.parse_line(self.nmea) and self.parser.valid: # O conteúdo é analisado
                        if self.parser.has_coordinates():
                            self.tl['values']['gps_sat'] = self.parser.satellites
                            self.tl['values']['gps_lat'] = self.parser.latitude
                            self.tl['values']['gps_lon'] = self.parser.longitude
                                
                        if self.parser.has_navigation():
                            self.tl['values']['gps_vel'] = self.parser.speed
                            self.tl['values']['gps_cur'] = self.parser.course
                        
                        if self.parser.has_3d_fix():
                            self.tl['values']['gps_alt'] = self.parser.altitude
                        r = True
                self.gcc += 1
                if self.gcc >= 500: # Força a limpeza da memória após 500 aquisições
                    gc.collect()
                    self.gcc = 0
            return r
        except Exception as e:
            print ("problemas com GPS")
            return False


    def atualizarRTC(self):
        '''
        Sincroniza o RTC com o timestamp do GPS, se possível
        Sempre chama atualizar()
        '''
        rtc = RTC() # Instância do RTC do uC
        if self.atualizar() and self.parser.has_coordinates():
            try:
                if self.parser.date and self.parser.time:
                    d = self.parser.date.decode()
                    t = self.parser.time.decode()
                    rtc.datetime((2000 + int(d[4:6], 10), int(d[2:4], 10), int(d[0:2], 10), 0,
                                int(t[0:2], 10), int(t[2:4], 10), int(t[4:6], 10), 0))
                    return True
                return False
            except ValueError as e:
                return False
        else:
            return False

