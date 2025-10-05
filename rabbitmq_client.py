import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
import json

class RabbitMQClient:
    def __init__(self, config: Dict[str, Any]):
        self.host = config['rabbitmq']['host']
        self.port = config['rabbitmq']['port']
        self.username = config['rabbitmq']['username']
        self.password = config['rabbitmq']['password']
        self.vhost = config['rabbitmq'].get('vhost', '/')
        self.management_port = config['rabbitmq'].get('management_port', 15672)
        
        # Базовый URL для Management API
        self.base_url = f"http://{self.host}:{self.management_port}/api"
        self.auth = aiohttp.BasicAuth(self.username, self.password)
    
    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Выполняет HTTP запрос к RabbitMQ Management API"""
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    async def get_exchanges(self) -> List[Dict[str, Any]]:
        """Получает список всех обменов"""
        try:
            exchanges = await self._make_request(f"exchanges/{self.vhost}")
            # Фильтруем системные обмены
            return [ex for ex in exchanges if not ex['name'].startswith('amq.')]
        except Exception as e:
            print(f"Ошибка при получении обменов: {e}")
            return []
    
    async def get_queues(self) -> List[Dict[str, Any]]:
        """Получает список всех очередей"""
        try:
            return await self._make_request(f"queues/{self.vhost}")
        except Exception as e:
            print(f"Ошибка при получении очередей: {e}")
            return []
    
    async def get_bindings(self) -> List[Dict[str, Any]]:
        """Получает список всех привязок"""
        try:
            return await self._make_request(f"bindings/{self.vhost}")
        except Exception as e:
            print(f"Ошибка при получении привязок: {e}")
            return []
    
    async def get_topology(self) -> Dict[str, Any]:
        """Получает полную топологию RabbitMQ"""
        try:
            exchanges, queues, bindings = await asyncio.gather(
                self.get_exchanges(),
                self.get_queues(),
                self.get_bindings()
            )
            
            return {
                "exchanges": exchanges,
                "queues": queues,
                "bindings": bindings,
                "connections": self._build_connections(exchanges, queues, bindings)
            }
        except Exception as e:
            print(f"Ошибка при получении топологии: {e}")
            return {"exchanges": [], "queues": [], "bindings": [], "connections": []}
    
    def _build_connections(self, exchanges: List[Dict], queues: List[Dict], bindings: List[Dict]) -> List[Dict[str, Any]]:
        """Строит связи между обменами и очередями на основе привязок"""
        connections = []
        
        for binding in bindings:
            source = binding.get('source', '')
            destination = binding.get('destination', '')
            destination_type = binding.get('destination_type', '')
            
            # Находим соответствующие обмены и очереди
            source_exchange = next((ex for ex in exchanges if ex['name'] == source), None)
            dest_queue = next((q for q in queues if q['name'] == destination), None)
            
            if source_exchange and dest_queue:
                connections.append({
                    'from': {
                        'type': 'exchange',
                        'name': source,
                        'id': f"exchange_{source}"
                    },
                    'to': {
                        'type': 'queue',
                        'name': destination,
                        'id': f"queue_{destination}"
                    },
                    'routing_key': binding.get('routing_key', ''),
                    'arguments': binding.get('arguments', {})
                })
        
        return connections
