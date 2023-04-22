import logging as log

log.basicConfig(format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                level=log.DEBUG,
                datefmt='%I:%M:%S %p',
                encoding='UTF-8',
                handlers=[
                    log.FileHandler('Logging/capa_datos.log'),
                    log.StreamHandler()
                ])


if __name__ == '__main__':
    log.debug('Mensaje a Nivel Debug')
    log.info('Mensaje a nivel de Info')
    log.warning('Mensaje a nivel de Warning')
    log.error('Mensaje a nivel de Error')
    log.critical('Mensaje a nivel Critico')
