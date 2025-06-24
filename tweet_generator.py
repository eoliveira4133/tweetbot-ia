import random
import requests
import json
from typing import List, Dict

class TweetGenerator:
    def __init__(self):
        # Templates de tweets para diferentes tópicos de empreendedorismo digital
        self.templates = {
            'produtividade': [
                "🚀 Dica de produtividade: {tip}. Qual é a sua estratégia favorita? #Produtividade #Empreendedorismo",
                "⏰ Tempo é dinheiro! {tip} #TimeManagement #Empreendedor",
                "💡 Hack de produtividade: {tip}. Teste e me conte o resultado! #ProductivityHack"
            ],
            'mindset': [
                "🧠 Mindset empreendedor: {insight}. Concorda? #Mindset #Empreendedorismo",
                "💪 {insight} - essa é a mentalidade que separa os vencedores! #MindsetEmpreendedor",
                "🎯 Lembre-se: {insight} #Motivacao #Empreendedor"
            ],
            'marketing': [
                "📈 Estratégia de marketing: {strategy}. Já testou? #MarketingDigital #Empreendedorismo",
                "🎯 {strategy} - essa tática pode revolucionar seu negócio! #Marketing",
                "💰 Quer mais vendas? {strategy} #VendasOnline #MarketingDigital"
            ],
            'tecnologia': [
                "🤖 Tecnologia para empreendedores: {tech_tip}. Conhece outras? #TechEmpreendedor #IA",
                "⚡ {tech_tip} - a tecnologia a favor do seu negócio! #Tecnologia #Automacao",
                "🔧 Ferramenta essencial: {tech_tip} #FerramentasDigitais #Empreendedorismo"
            ]
        }
        
        # Conteúdo para preencher os templates
        self.content_data = {
            'tip': [
                "Use a técnica Pomodoro para focar em blocos de 25 minutos",
                "Automatize tarefas repetitivas com ferramentas de IA",
                "Defina apenas 3 prioridades por dia",
                "Elimine notificações desnecessárias durante o trabalho",
                "Use templates para acelerar processos recorrentes"
            ],
            'insight': [
                "O fracasso é apenas feedback disfarçado",
                "Consistência vence talento quando o talento não é consistente",
                "Seu maior concorrente é a versão de ontem de você mesmo",
                "Problemas são oportunidades de negócio esperando para serem descobertas",
                "A ação imperfeita é melhor que a perfeição inativa"
            ],
            'strategy': [
                "Crie conteúdo de valor antes de vender qualquer coisa",
                "Use stories para humanizar sua marca",
                "Teste diferentes horários de postagem para encontrar seu público",
                "Responda todos os comentários nas primeiras 2 horas",
                "Colabore com outros criadores do seu nicho"
            ],
            'tech_tip': [
                "ChatGPT para criar conteúdo e automatizar respostas",
                "Zapier para conectar suas ferramentas favoritas",
                "Canva para criar designs profissionais em minutos",
                "Google Analytics para entender seu público",
                "Buffer para agendar posts em todas as redes sociais"
            ]
        }
        
        # Hashtags populares por categoria
        self.hashtags = {
            'produtividade': ['#Produtividade', '#TimeManagement', '#Foco', '#Eficiencia'],
            'mindset': ['#Mindset', '#Motivacao', '#Sucesso', '#MindsetEmpreendedor'],
            'marketing': ['#MarketingDigital', '#VendasOnline', '#Marketing', '#ConteudoDigital'],
            'tecnologia': ['#IA', '#Automacao', '#TechEmpreendedor', '#FerramentasDigitais'],
            'geral': ['#Empreendedorismo', '#Empreendedor', '#NegociosOnline', '#DigitalBusiness']
        }
    
    def generate_tweet(self, topic: str = None) -> Dict[str, str]:
        """Gera um tweet baseado no tópico especificado ou aleatório"""
        if not topic:
            topic = random.choice(list(self.templates.keys()))
        
        # Seleciona template aleatório do tópico
        template = random.choice(self.templates[topic])
        
        # Preenche o template com conteúdo relevante
        if '{tip}' in template:
            content = template.format(tip=random.choice(self.content_data['tip']))
        elif '{insight}' in template:
            content = template.format(insight=random.choice(self.content_data['insight']))
        elif '{strategy}' in template:
            content = template.format(strategy=random.choice(self.content_data['strategy']))
        elif '{tech_tip}' in template:
            content = template.format(tech_tip=random.choice(self.content_data['tech_tip']))
        else:
            content = template
        
        # Adiciona hashtags específicas do tópico + hashtags gerais
        topic_hashtags = random.sample(self.hashtags[topic], 2)
        general_hashtags = random.sample(self.hashtags['geral'], 1)
        all_hashtags = topic_hashtags + general_hashtags
        
        # Garante que o tweet não exceda 280 caracteres
        hashtag_string = ' '.join(all_hashtags)
        if len(content + ' ' + hashtag_string) > 280:
            # Remove hashtags se necessário
            content = content[:250] + '...'
            hashtag_string = ' '.join(all_hashtags[:2])
        
        return {
            'content': content,
            'hashtags': hashtag_string,
            'topic': topic,
            'full_tweet': content + ' ' + hashtag_string
        }
    
    def generate_multiple_tweets(self, count: int = 5, topics: List[str] = None) -> List[Dict[str, str]]:
        """Gera múltiplos tweets"""
        tweets = []
        for _ in range(count):
            topic = random.choice(topics) if topics else None
            tweets.append(self.generate_tweet(topic))
        return tweets
    
    def add_affiliate_link(self, tweet_content: str, product_type: str = 'curso') -> str:
        """Adiciona link de afiliado estrategicamente ao tweet"""
        affiliate_links = {
            'curso': 'https://bit.ly/curso-empreendedor-digital',
            'ferramenta': 'https://bit.ly/ferramentas-produtividade',
            'ebook': 'https://bit.ly/ebook-marketing-digital',
            'consultoria': 'https://bit.ly/consultoria-negocios'
        }
        
        cta_phrases = [
            "Saiba mais:",
            "Descubra como:",
            "Acesse aqui:",
            "Link na bio:",
            "Clique aqui:"
        ]
        
        link = affiliate_links.get(product_type, affiliate_links['curso'])
        cta = random.choice(cta_phrases)
        
        # Adiciona o link se houver espaço
        full_content = f"{tweet_content}\n\n{cta} {link}"
        
        if len(full_content) <= 280:
            return full_content
        else:
            return tweet_content  # Retorna sem link se exceder limite

