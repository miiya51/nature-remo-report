from setting import NATURE_REMO, INTERVAL_MINUTES, Base, api, engine, logger, my_log, tz_jst_name
from sqlalchemy.orm import Session
import schedule
import time

class REMO_EX:
    def __init__(self) -> None:
        Base.metadata.create_all(engine)
        self.logo_ascii = """
         .(.dWHHQ,.
            WN,  dM[
            -Hb .mH%
           .WMNNH#^ .WMMm, (TNa..dNa.dmJ.   ..,.
          .dgf?TN,  WMHMH%   ,MMHHMMNMMMl .HH#W"BQ,
         .WM%   ,WQ-JMe..    (NNFJMNHUHH} ,MH    .MN
                      .7"=  ,MNM!_TB= TMN.. TNggHHM=

                                    .      (m,                                                    
                 .dgMMMg,   .,    .XqR.    ,Hb         ....                         dm.
                dqHY!  (MN.  ,Ha..mgf  (WNMMMMMMM$ zm-WMB"?Mx  ..,       +MMa,      dMl..
               .mmP  .dgg@     TMNgY       .HM     ,MMHl    ?'.qY?Mg,   J@%  Tb .(kMMMY?7
                4Mb7WMMY^     .XMMb        .@M      MNP      .gP  (M#   MM          W#:
                 (Wa......   .gg@ ?H,      ,H@      MM]      ,@l .XMM,  MN          MM
                    _'''9"^   ?=           MMl      dMF      ,H).WK' ?''TM,        .##
                                                     -^       TMHY       ?M,....   .H#
                                                                                   ,H@
                                                                                   JMF
"""
        self.print_logo()

    @my_log(logger)
    def print_logo(self) -> None:
        logger.info(self.logo_ascii)

    @my_log(logger)
    def fetch_devices_info(self):
        devices = api.get_devices()
        return devices

    @staticmethod
    @my_log(logger)
    def make_devices(device):
        id = device.id
        get_time = device.newest_events["te"].created_at.astimezone(tz_jst_name)
        name = device.name
        temp = device.newest_events["te"].val
        #logger.debug(id, get_time, name, temp)
        record = NATURE_REMO(id=id, get_time=get_time, device_name=name, temp=temp)
        return record

    @my_log(logger)
    def run(self):
        devices = self.fetch_devices_info()
        with Session(engine) as session:
            for device in devices:
                record = self.make_devices(device)
                session.add(record)
            session.commit()


def __main__():
    remo_ex = REMO_EX()
    remo_ex.run()
    schedule.every(INTERVAL_MINUTES).minutes.do(remo_ex.run)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    __main__()
