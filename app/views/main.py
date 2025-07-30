"""
Main Views - Basic application routes
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/train_finder')
def train_finder():
    """Train finder page"""
    return render_template('train_finder.html')

@main_bp.route('/trainstatus')
def train_status():
    """Train status page"""
    return render_template('running_status.html', form=True) 