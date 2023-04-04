import os

# Definir caminho absoluto para o arquivo de log
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'infos.log')

# Configurar handler de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': log_path,
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'discord': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
