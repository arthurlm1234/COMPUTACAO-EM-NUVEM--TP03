import numpy as np

def handler(entrada: dict, contexto: object) -> dict:

    nb_cpus = 16
    porcentagens_cpu = [entrada.get(f'cpu_percent-{i}', 0) for i in range(nb_cpus)]

    memoria_virtual_total = entrada.get('virtual_memory-total', 0)
    memoria_virtual_buffers = entrada.get('virtual_memory-buffers', 0)
    memoria_virtual_cached = entrada.get('virtual_memory-cached', 0)

    bytes_enviados = entrada.get('net_io_counters_eth0-packets_sent', 0)
    bytes_recebidos = entrada.get('net_io_counters_eth0-packets_recv', 0)

    total_bytes = bytes_enviados + bytes_recebidos
    porcentagem_egresso_rede = (bytes_enviados / total_bytes) * 100 if total_bytes > 0 else 0

    porcentagem_cache_memoria = ((memoria_virtual_buffers + memoria_virtual_cached) / memoria_virtual_total) * 100 if memoria_virtual_total > 0 else 0

    medias_moveis_simples = []
    for i, porcentagem_cpu_X in enumerate(porcentagens_cpu):
        utilizacoes_X = contexto.env.get(f'cpu{i}_utilizations', [])
        utilizacoes_X.append(porcentagem_cpu_X)
        
        if len(utilizacoes_X) > 60:
            utilizacoes_X.pop(0)
        
        contexto.env[f'cpu{i}_utilizations'] = utilizacoes_X
        media_movel_simples_X = np.mean(utilizacoes_X)
        medias_moveis_simples.append(media_movel_simples_X)
        
    resposta = {
        'porcentagem-rede-egresso': porcentagem_egresso_rede,
        'porcentagem-cache-memoria': porcentagem_cache_memoria
    }

    resposta.update({f'media-movel-cpu{i}': media_movel_simples_X for i, media_movel_simples_X in enumerate(medias_moveis_simples)})

    return resposta
