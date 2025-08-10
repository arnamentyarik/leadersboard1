
from flask import jsonify, request
from app import app
from models import Player

@app.route('/api/leaderboard')
def api_leaderboard():
        # остальной код остается без изменений
    """API endpoint for leaderboard data with fallback"""
    try:
        sort_by = request.args.get('sort', 'experience')
        limit = min(int(request.args.get('limit', 50)), 100)
        
        players = Player.get_leaderboard(sort_by=sort_by, limit=limit) or []
        
        # Convert players to dict format
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'nickname': player.nickname,
                'level': player.level,
                'experience': player.experience,
                'kills': player.kills,
                'deaths': player.deaths,
                'wins': player.wins,
                'games_played': player.games_played,
                'kd_ratio': player.kd_ratio,
                'win_rate': player.win_rate
            })
        
        return jsonify({
            'success': True,
            'players': players_data,
            'total': len(players_data)
        })
    except Exception as e:
        app.logger.error(f"Error in API leaderboard: {e}")
        return jsonify({
            'success': False,
            'players': [],
            'total': 0,
            'error': 'Failed to load leaderboard data'
        }), 200  # Still return 200 with empty data
from flask import jsonify, request
from app import app
from models import Player

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data with fallback"""
    try:
        sort_by = request.args.get('sort', 'experience')
        limit = min(int(request.args.get('limit', 50)), 100)
        
        players = Player.get_leaderboard(sort_by=sort_by, limit=limit) or []
        
        # Convert players to dict format
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'nickname': player.nickname,
                'level': player.level,
                'experience': player.experience,
                'kills': player.kills,
                'deaths': player.deaths,
                'wins': player.wins,
                'games_played': player.games_played,
                'kd_ratio': player.kd_ratio,
                'win_rate': player.win_rate
            })
        
        return jsonify({
            'success': True,
            'players': players_data,
            'total': len(players_data)
        })
    except Exception as e:
        app.logger.error(f"Error in API leaderboard: {e}")
        return jsonify({
            'success': False,
            'players': [],
            'total': 0,
            'error': 'Failed to load leaderboard data'
        }), 200  # Still return 200 with empty data

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics data"""
    try:
        stats = Player.get_statistics()
        
        # Get top players for charts
        top_exp_players = Player.get_leaderboard('experience', 5)
        top_kills_players = Player.get_leaderboard('kills', 5)
        top_final_kills_players = Player.get_leaderboard('final_kills', 5)
        top_beds_players = Player.get_leaderboard('beds_broken', 5)
        top_wins_players = Player.get_leaderboard('wins', 5)
        
        # Player level distribution
        level_distribution = {}
        all_players = Player.query.all()
        for player in all_players:
            level = player.level
            if level <= 10:
                category = "1-10"
            elif level <= 25:
                category = "11-25"
            elif level <= 50:
                category = "26-50"
            elif level <= 100:
                category = "51-100"
            elif level <= 200:
                category = "101-200"
            else:
                category = "200+"
            
            level_distribution[category] = level_distribution.get(category, 0) + 1
        
        charts_data = {
            'top_players_exp': {
                'labels': [p.nickname for p in top_exp_players],
                'data': [p.experience for p in top_exp_players]
            },
            'top_players_kills': {
                'labels': [p.nickname for p in top_kills_players],
                'data': [p.kills for p in top_kills_players]
            },
            'top_players_final_kills': {
                'labels': [p.nickname for p in top_final_kills_players],
                'data': [p.final_kills for p in top_final_kills_players]
            },
            'top_players_beds': {
                'labels': [p.nickname for p in top_beds_players],
                'data': [p.beds_broken for p in top_beds_players]
            },
            'top_players_wins': {
                'labels': [p.nickname for p in top_wins_players],
                'data': [p.wins for p in top_wins_players]
            },
            'player_levels': level_distribution
        }
        
        # Top 3 players for carousel
        top_3_players = Player.get_leaderboard('experience', 3)
        top_players_carousel = []
        for i, player in enumerate(top_3_players):
            top_players_carousel.append({
                'id': player.id,
                'nickname': player.nickname,
                'level': player.level,
                'experience': player.experience,
                'kills': player.kills,
                'final_kills': player.final_kills,
                'deaths': player.deaths,
                'beds_broken': player.beds_broken,
                'wins': player.wins,
                'games_played': player.games_played,
                'kd_ratio': player.kd_ratio,
                'fkd_ratio': player.fkd_ratio,
                'win_rate': player.win_rate,
                'skin_url': player.minecraft_skin_url,
                'role': player.display_role,
                'star_rating': player.star_rating,
                'rank': i + 1
            })
        
        return jsonify({
            'success': True,
            'stats': stats,
            'charts': charts_data,
            'top_players_carousel': top_players_carousel
        })
        
    except Exception as e:
        app.logger.error(f"Error in API stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'stats': {},
            'charts': {},
            'top_players_carousel': []
        }), 200
