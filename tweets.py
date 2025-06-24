from flask import Blueprint, request, jsonify
from src.models.tweet import db, Tweet, User
from src.services.tweet_generator import TweetGenerator
import random

tweet_bp = Blueprint('tweets', __name__)
generator = TweetGenerator()

@tweet_bp.route('/generate', methods=['POST'])
def generate_tweet():
    """Gera um tweet baseado nos parâmetros fornecidos"""
    try:
        data = request.get_json() or {}
        topic = data.get('topic')
        include_affiliate = data.get('include_affiliate', False)
        product_type = data.get('product_type', 'curso')
        
        # Gera o tweet
        tweet_data = generator.generate_tweet(topic)
        
        # Adiciona link de afiliado se solicitado
        if include_affiliate:
            tweet_data['full_tweet'] = generator.add_affiliate_link(
                tweet_data['full_tweet'], 
                product_type
            )
        
        # Salva no banco de dados
        new_tweet = Tweet(
            content=tweet_data['content'],
            hashtags=tweet_data['hashtags'],
            topic=tweet_data['topic']
        )
        db.session.add(new_tweet)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tweet': tweet_data,
            'id': new_tweet.id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tweet_bp.route('/generate-batch', methods=['POST'])
def generate_batch():
    """Gera múltiplos tweets de uma vez"""
    try:
        data = request.get_json() or {}
        count = min(data.get('count', 5), 20)  # Máximo 20 tweets por vez
        topics = data.get('topics', [])
        include_affiliate = data.get('include_affiliate', False)
        
        tweets = generator.generate_multiple_tweets(count, topics if topics else None)
        
        # Salva todos os tweets no banco
        saved_tweets = []
        for tweet_data in tweets:
            if include_affiliate and random.random() < 0.3:  # 30% chance de incluir link
                tweet_data['full_tweet'] = generator.add_affiliate_link(
                    tweet_data['full_tweet']
                )
            
            new_tweet = Tweet(
                content=tweet_data['content'],
                hashtags=tweet_data['hashtags'],
                topic=tweet_data['topic']
            )
            db.session.add(new_tweet)
            saved_tweets.append(tweet_data)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tweets': saved_tweets,
            'count': len(saved_tweets)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tweet_bp.route('/history', methods=['GET'])
def get_tweet_history():
    """Retorna histórico de tweets gerados"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        
        tweets = Tweet.query.order_by(Tweet.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'tweets': [tweet.to_dict() for tweet in tweets.items],
            'total': tweets.total,
            'pages': tweets.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tweet_bp.route('/topics', methods=['GET'])
def get_available_topics():
    """Retorna tópicos disponíveis para geração"""
    topics = list(generator.templates.keys())
    return jsonify({
        'success': True,
        'topics': topics
    })

@tweet_bp.route('/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas de uso"""
    try:
        total_tweets = Tweet.query.count()
        published_tweets = Tweet.query.filter_by(published=True).count()
        topics_stats = db.session.query(
            Tweet.topic, 
            db.func.count(Tweet.id).label('count')
        ).group_by(Tweet.topic).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_tweets': total_tweets,
                'published_tweets': published_tweets,
                'unpublished_tweets': total_tweets - published_tweets,
                'topics_breakdown': [
                    {'topic': topic, 'count': count} 
                    for topic, count in topics_stats
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tweet_bp.route('/demo', methods=['GET'])
def demo():
    """Endpoint de demonstração que gera tweets de exemplo"""
    try:
        # Gera 3 tweets de exemplo de diferentes tópicos
        demo_topics = ['produtividade', 'mindset', 'marketing']
        demo_tweets = []
        
        for topic in demo_topics:
            tweet_data = generator.generate_tweet(topic)
            # Adiciona link de afiliado em um dos tweets para demonstração
            if topic == 'marketing':
                tweet_data['full_tweet'] = generator.add_affiliate_link(
                    tweet_data['full_tweet'], 'curso'
                )
                tweet_data['has_affiliate'] = True
            else:
                tweet_data['has_affiliate'] = False
            
            demo_tweets.append(tweet_data)
        
        return jsonify({
            'success': True,
            'message': 'Tweets de demonstração gerados com sucesso!',
            'demo_tweets': demo_tweets,
            'monetization_info': {
                'affiliate_potential': 'Links de afiliados podem gerar 5-15% de comissão',
                'subscription_model': 'Usuários pagam R$19-49/mês por acesso ilimitado',
                'lead_generation': 'Tweets podem direcionar para landing pages de captura'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

