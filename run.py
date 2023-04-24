import xml.etree.ElementTree as ET

# Define o nome do arquivo de perfil do Proxifier
filename = 'Default.ppx'

# Carrega o arquivo XML do perfil do Proxifier
tree = ET.parse(filename)
root = tree.getroot()

# Obtém o ID do último proxy existente, ou 100 caso não exista nenhum
proxy_elem = root.find('.//Proxy')
if proxy_elem is not None:
    proxy_id = int(proxy_elem.get('id')) + 1
else:
    proxy_id = 100

# Loop para adicionar todos os proxies do arquivo 'proxies.txt'
with open('proxies.txt', 'r') as f:
    for line in f:
        # Cria um novo proxy com as informações do arquivo txt
        proxy = ET.Element('Proxy')
        proxy.set('id', str(proxy_id))
        proxy.set('type', 'SOCKS5')
        address, port = line.strip().split(':')
        ET.SubElement(proxy, 'Address').text = address
        ET.SubElement(proxy, 'Port').text = port
        root.find('.//ProxyList').append(proxy)

        # Adiciona o novo proxy à chain existente
        chain_id = '102'
        chain = root.find(f'.//Chain[@id="{chain_id}"]')
        if chain is not None:
            new_proxy = ET.Element('Proxy')
            new_proxy.set('enabled', 'true')
            new_proxy.text = proxy.get('id')
            chain.append(new_proxy)

        # Incrementa a variável de ID para o próximo proxy a ser adicionado
        proxy_id += 1

# Salva as alterações no arquivo XML do perfil do Proxifier
tree.write(filename)
