from flask import Flask, jsonify
from api.github import get_github_user_stats, get_starred_repos, get_user_organizations

app = Flask(__name__)

@app.route("/stats/<username>")
def github_stats(username):
    """Fetch GitHub stats for a given user."""
    user_stats = get_github_user_stats(username)
    if not  user_stats:
        return jsonify({"error": "User not found"}), 404
 # Fetch additional stats
    starred_repos = get_starred_repos(username)
    organizations = get_user_organizations(username)

    # Combine all stats
    user_stats["starred_repos"] = starred_repos
    user_stats["organizations"] = organizations
    
    return jsonify(user_stats)
    
if __name__ == "__main__":
    app.run(debug=True)
