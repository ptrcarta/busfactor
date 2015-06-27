from flask import render_template
from random import random
import colorsys as cs

def rgb_to_web(c):
    """[0,1) rgb tuple to web colorcode"""
    scaled = map(lambda x: round(x*255), c)
    return "#" + "%02x"*3 % tuple(scaled)

def get_color(c):
    #scale the logistic function properly
    #f =  lambda x :logistic.cdf(x*8)
    return cs.hsv_to_rgb((f(c))*3.4/10, 1, 1- 0.2*random(1)[0])


test_projects = [
        {'name':'gogs',
        'owner':'gogits',
        'factor':1,
        'contributors_num':193,
        'contributors': [
            {'login':'random_guy1',
            'percentage':85
            },
            {'login':'random_guy2',
            'percentage':10
            },
            {'login':'random_guy3',
            'percentage':2
            },
            {'login':'random_guy4',
            'percentage':1
            },
            {'login':'others',
            'percentage':1
            }
        ]},
        {'name':'fish-shell',
        'owner':'fish-shell',
        'factor':5,
        'contributors_num':193,
        'contributors': [
            {'login':'random_guy1',
            'percentage':30
            },
            {'login':'random_guy2',
            'percentage':20
            },
            {'login':'random_guy3',
            'percentage':20
            },
            {'login':'random_guy4',
            'percentage':10
            },
            {'login':'random_guy5',
            'percentage':10
            },
            {'login':'others',
            'percentage':10
            }
        ]},
        {'name':'ipfs',
        'owner':'go-ipfs',
        'factor':18,
        'contributors_num':53,
        'contributors': [
            {
            'login':'random_guy',
            'percentage':5} for i in range(18)
            ] + [{'login':'others', 'percentage':10}]} ]

def register_views(app):
    @app.route("/")
    def index():
        return render_template('index.html', projects=test_projects)
