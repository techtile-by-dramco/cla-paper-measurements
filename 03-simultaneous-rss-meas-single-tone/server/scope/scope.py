import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa
import numpy as np # http://www.numpy.org/
from scipy.signal import find_peaks

from enum import Enum
class ScopeMode(Enum):
    # TODO
    POWER = 1

class Scope:
    """_summary_

    Usage:
        scope = Scope("192.108.0.251")
        power_dBm = scope.get_power_dBm()
    """
    def __init__(self, ip:str, mode:ScopeMode=ScopeMode.POWER) -> None:
        self.visa_address = f'TCPIP::{ip}::INSTR'

        self.span = None
    
        #self.setup()
    
    def write(self, s:str):
        self.scope.write(s)

    def query(self, s:str):
        return self.scope.query(s)

    def setup(self, bandwidth, center, span, rbw):

        self.span = span
        self.rbw = rbw

        #TODO make this configurable
        rm = visa.ResourceManager()
        self.scope = rm.open_resource(self.visa_address)

        print(self.scope)

        self.scope.timeout = 10000 # ms
        self.scope.encoding = 'latin_1'
        self.scope.read_termination = '\n'
        self.scope.write_termination = None
        self.write('*cls') # clear ESR
        self.write('*rst') # reset
        _ = self.query('*opc?') # sync

        channel_list = [1,2]

        for channel in channel_list:

            # Channel 1 50Ohm 2GHz
            self.write(f"DISplay:GLObal:CH{channel}:STATE ON")
            self.write(f"CH{channel}:TERMINATION 50")
            self.write(f"CH{channel}:BANDWIDTH {bandwidth}")
            
            # open spectrum view
            # spectrum view 910MHz and 100kHz BW
            self.write(f"DISplay:SELect:SPECView1:SOUrce CH{channel}")
            self.write(f"CH{channel}:SV:STATE ON")
            self.write(f"CH{channel}:SV:CENTERFrequency {center}")
            self.write(f"SV:SPAN {span}")

            self.write(f"DATa:SOUrce CH{channel}_SV_NORMal")

            # self.write("MEASUREMENT:ADDMEAS CPOWER")

            if channel == 1:
                self.write(f"SV:RBWMode MANUAL")
                self.write(f"SV:RBW {self.rbw}")

                #test
            self.write(f"SV:CH{channel}:UNIts DBM")

            time.sleep(1)

            channel_width = 2E3

            # self.write("ACQUIRE:STATE ON")

            self.write("MEASUREMENT:ADDMEAS PHASE")

            self.write(f"MEASUREMENT:MEAS{channel}:TYPE CPOWER")
            # self.write(f"MEASUREMENT:MEAS{channel}:SOURCE CH{channel}")
            self.write(f"MEASUREMENT:MEAS{channel}:SOURCE CH{channel}_SV_NORMAL")

            self.write(f"SV:CH{channel}:UNIts DBM")

            time.sleep(0.1)

            self.write(f"MEASUREMENT:MEAS{channel}:CPWIDTh {channel_width}")

            self.write(f"MEASUREMENT:MEAS{channel}:ABANdwidth {channel_width}")
            
            # print(self.query(f"MEASUREMENT:MEAS{channel}:CPWIDTh {channel_width}"))
            
            # time.sleep(1)

            # print(self.query("MEASUREMENT:IMMED:VALUE?"))


            # self.write(f"DATa:SOUrce CH{channel}_SV_NORMal")
            # self.write(f"DISplay:SPECView1:VIEWStyle OVErlay")
        # data_stop = round(self.span/self.rbw*2)
        # self.write(f"DATa:START 1")
        # self.write(f"DATa:STOP {data_stop}")#1901
                #test

        #     self.write(f"SV:CH{channel}:UNIts DBM")

        #     self.write(f"DATa:SOUrce CH{channel}_SV_NORMal")
        
        # self.write(f"DISplay:SPECView1:VIEWStyle OVErlay")

        # data_stop = round(self.span/self.rbw*2)

        # self.write(f"DATa:START 1")
        # self.write(f"DATa:STOP {data_stop}")#1901

        # print(self.query(f"DISplay:SPECView1:CURSor:CURSOR:BSOUrce?"))

        # self.write(f"DISplay:SPECView1:CURSor:CURSOR:BSOUrce CH1")#1901
        
        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH1")
        # self.write(f"DATa:SOUrce CH1_SV_NORMal")

        # # Add new measurement phase
        # self.write("MEASUREMENT:ADDMEAS CPOWER")

        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH2")
        # self.write(f"DATa:SOUrce CH2_SV_NORMal")

        # # Add new measurement phase
        # self.write("MEASUREMENT:ADDMEAS CPOWER")



        # time.sleep(1)

        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH2")

        # time.sleep(1)

        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH1")


        self.write(f"WFMOutpre:BYT_Or LSB")

        _ = self.query('*opc?') # sync

        # self.write("HORIZONTAL:RECORDLENGTH 1000")
        # self.write("ACQUIRE:MODE SAMPLE")
        # self.write("ACQUIRE:STOPAFTER SEQUENCE")


        # # Trigger a new acquisition if necessary
        self.write("ACQuire:STATE ON")
        
        # Ensure the acquisition is complete
        self.query("*OPC?")  # Wait for operation to complete


        active_measurements = self.query("MEASUrement:LIST?").replace('\n', '').split(',')

        # self.write("MEASTABle:ADDNew 'TABLE1'")
        # MEASTABle

        # time.sleep(1)
        # print(self.query("MEASUrement?"))

        # exit()

        # self.write("MEASUREMENT:ADDMEAS PHASE")

        while 1:
            # active_measurements = self.query("MEASUrement:LIST?").replace('\n', '').split(',')
            # print(self.query("MEASUrement:LIST?").replace('\n', '').split(','))
            time.sleep(2)

            print('***** Measurement List:')
            print(self.query('MEASUrement:LIST?'))

            print('***** Value: PK2PK Measurement:')
            print(self.query('MEASUrement:MEAS1:VALUE?'))

            print('***** Measurement with stats:')
            print(self.query('MEASUrement:MEAS1:RESULTS:ALLACQS:MEAN?;MINI?;MAX?;STDDEV?;POPU?'))

            print('***** Measurement with unit and other tags:')
            print(self.query('MEASUrement:MEAS1:VALUE?;XUNIT?;YUNIT?;TYPE?;SOUR1?;SOUR2?'))

            print(self.query("MEASUREMENT:IMMED:VALUE?"))

            # print(self.query("DATa:SOUrce:AVAILable?"))

            # for meas_name in active_measurements:
            #     print(meas_name)
            #     self.query("*OPC?")
            #     print(self.query(f"MEASUrement:{meas_name}:RESUlts:CURRentacq:MEAN?"))
                
            # print(self.query(f"MEASUrement:MEAS2:RESUlts:HISTory:MEAN?"))

                # print(self.query('CUSTOMTABle:LIST?'))
        


    def get_power_dBm(self, cable_loss) -> float:
        pwr_dbm = self.scope.query_binary_values("CURVe?", datatype='d', container=np.array)
        pwr_lin = 10 ** (pwr_dbm / 10)
        tot_pwr_dbm = float(10*np.log10(np.sum(pwr_lin))) #float to cast to single element
        return tot_pwr_dbm + cable_loss


    def get_power_dBm_peaks(self, cable_loss, search_for_no_peaks) -> float:

        #   Check span adjustments externally
        self.check_span()

        #   Get spectrum form scope
        self.write(f"DATa:SOUrce CH1_SV_NORMal")
        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH1")
        pwr_dbm = self.scope.query_binary_values("CURVe?", datatype='d', container=np.array)
        
        # #   Calculate all peaks in spectrum
        # peaks,_ = find_peaks(pwr_dbm)
        # #print(pwr_dbm[peaks])

        # #   Sort peaks in descending order
        # peaks_sorted = sorted(pwr_dbm[peaks], reverse=True)
        # # print(peaks_sorted[:search_for_no_peaks])

        # #   Combine peaks to one overall power value
        # power_linear = 10 ** (np.asarray(peaks_sorted[:search_for_no_peaks]) / 10)
        # #print(power_linear)
        # tot_pwr_dbm = float(10*np.log10(np.sum(power_linear))) #float to cast to single element
        
        # return tot_pwr_dbm + cable_loss, peaks        

        # print(pwr_dbm)

        return np.max(pwr_dbm)
    

    def get_channel_peak_power_dBm(self, channel) -> float:

        # #   Check span adjustments externally
        # self.check_span()

        # #   Get spectrum form scope
        # self.write(f"DISplay:SELect:SPECView1:SOUrce CH{channel}")
        # self.write(f"DATa:SOUrce CH{channel}_SV_NORMal")
        # pwr_dbm = self.scope.query_binary_values("CURVe?", datatype='d', container=np.array)

        return self.query("MEASUrement:LIST?").replace('\n', '').split(',')[-1]
        



    def check_span(self):
        new_span = float(self.query(f"SV:SPAN?"))
        if new_span != self.span:
            
            #   Warning
            print("Span changed externally!")

            #   Update span value
            self.span = new_span

            data_stop = round(self.span/self.rbw*2)

            self.write(f"DATa:START 1")
            self.write(f"DATa:STOP {data_stop}")#1901