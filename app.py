from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import random

app = Flask(__name__, static_folder='static')
CORS(app)

OPENWEATHERMAP_API_KEY = "f4a1438eb714927086d43d404e975cc3"

# Base de datos de productos.
products = {
    # Paletas a base de agua
    "Paleta de Limón": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una paleta clásica y refrescante, ideal para un día caluroso.",
        "image_url": "/static/images/1.jpeg" , "price": "20"
    },
    "Paleta de Mango": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor dulce y tropical que te transportará a un paraíso.",
        "image_url": "/static/images/2.jpeg", "price": "20"
    },
    "Paleta de Uva": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "El sabor dulce y familiar que siempre es una buena opción.",
        "image_url": "/static/images/3.jpeg", "price": "20"
    },
    "Paleta de Sandía": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Una paleta jugosa y refrescante con un sabor auténtico a sandía.",
        "image_url": "/static/images/4.jpeg", "price": "20"
    },
    "Paleta de Guayaba": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor tropical y exótico, suave y lleno de sabor a fruta.",
        "image_url": "/static/images/5.jpeg", "price": "20"
    },
    "Paleta de Chicle": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Original",
        "reason": "Una paleta divertida y con un sabor muy original que te recordará a la infancia.",
        "image_url": "/static/images/6.jpeg", "price": "20"
    },
    "Paleta de Fresa (agua)": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "El sabor de la fresa en una versión ligera y refrescante.",
        "image_url": "/static/images/7.jpeg", "price": "25"
    },
    "Paleta de Guanábana": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor exótico y cremoso, a pesar de ser de agua. Una opción suave y deliciosa.",
        "image_url": "/static/images/8.jpeg", "price": "25"
    },
    "Paleta de Skwinkles": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Original",
        "reason": "Una explosión de sabor ácido y picante con un toque de dulce. ¡Para los valientes!",
        "image_url": "/static/images/9.jpeg", "price": "25"
    },
    "Paleta de Piña": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Un sabor ácido y refrescante, perfecto para limpiar el paladar.",
        "image_url": "/static/images/10.jpeg", "price": "20"
    },
    "Paleta de Grosella": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "El sabor único de la grosella en una paleta que te hará agua la boca.",
        "image_url": "/static/images/11.jpeg", "price": "20"
    },
    "Paleta de Tamarindo": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Un sabor ácido y agridulce que te transportará a los dulces típicos mexicanos.",
        "image_url": "/static/images/12.jpeg", "price": "20"
    },
    "Paleta de Mango con Chamoy": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Clásico",
        "reason": "La combinación perfecta de lo dulce, lo ácido y lo picante.",
        "image_url": "/static/images/13.jpg", "price": "25"
    },
    "Paleta de Mango con Chile": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Clásico",
        "reason": "Un sabor audaz y refrescante que te hará sentir el picor del chile.",
        "image_url": "/static/images/14.jpeg", "price": "25"
    },
    "Paleta de Piña con Chile": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Clásico",
        "reason": "El equilibrio ideal entre lo dulce de la piña y el picante del chile.",
        "image_url": "/static/images/15.jpeg" , "price": "25"
    },
    "Paleta Tropical": {
        "type": "Paleta", "base": "Agua", "flavor": "Dulce", "style": "Original",
        "reason": "Una mezcla de frutas tropicales para un sabor exótico y refrescante.",
        "image_url": "/static/images/16.jpeg", "price": "25"
    },
    "Paleta de Pepino con Chile": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Original",
        "reason": "Un sabor inusual pero increíblemente refrescante y picante.",
        "image_url": "/static/images/17.jpeg", "price": "25"
    },
    "Paleta de Kiwi con Fresa": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Dulce"], "style": "Original",
        "reason": "Una combinación perfecta de lo ácido del kiwi y lo dulce de la fresa.",
        "image_url": "/static/images/18.jpeg", "price": "25"
    },
    "Paleta de Tamarindo con Chile": {
        "type": "Paleta", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Original",
        "reason": "La versión picante de un clásico agridulce, para un toque de emoción.",
        "image_url": "/static/images/19.jpeg", "price": "30"
    },
    "Paleta de Mandarina": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una paleta con el sabor cítrico y refrescante de la mandarina.",
        "image_url": "/static/images/20.jpeg", "price": "25"
    },
    "Paleta de Naranja": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "La paleta perfecta para quienes aman el sabor cítrico y refrescante.",
        "image_url": "/static/images/21.jpeg", "price": "20"
    },
    "Paleta de Jamaica": {
        "type": "Paleta", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una opción floral y ligeramente ácida que refresca al instante.",
        "image_url": "/static/images/22.jpeg", "price": "20"
    },

    # Paletas a base de leche
    "Paleta de Fresa con Crema": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El clásico sabor cremoso y dulce que todos amamos, perfecto para un antojo.",
        "image_url": "/static/images/23.jpeg", "price": "35"
    },
    "Paleta de Queso con Fresa": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Una combinación inusual pero deliciosa, el sabor salado del queso y lo dulce de la fresa.",
        "image_url": "/static/images/24.jpeg", "price": "35"
    },
    "Paleta de Yogurt con Fresa": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Ligera y con un toque ácido del yogurt, perfecta para un gusto menos dulce.",
        "image_url": "/static/images/25.jpeg", "price": "35"
    },
    "Paleta de Fresa (leche)": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El sabor de fresa en una versión más cremosa y suave.",
        "image_url": "/static/images/26.jpeg", "price": "30"
    },
    "Paleta de Chongos": {
        "type": "Paleta", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "Un postre tradicional mexicano, ahora en una paleta cremosa y dulce.",
        "image_url": "/static/images/27.jpeg", "price": "30"
    },
    "Paleta de Queso con Zarzamora": {
        "type": "Paleta", "base": "Leche", "flavor": ["Cremoso", "Dulce"], "style": "Original",
        "reason": "El contraste perfecto entre el sabor del queso y lo dulce y un poco ácido de la zarzamora.",
        "image_url": "/static/images/28.jpeg", "price": "35"
    },
    "Paleta de Vainilla": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "Un sabor suave y dulce que nunca decepciona.",
        "image_url": "/static/images/29.jpeg", "price": "05"
    },
    "Paleta de Chocolate": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "La paleta favorita de los amantes del chocolate. Cremosa y deliciosa.",
        "image_url": "/static/images/30.jpeg", "price": "30"
    },
    "Paleta de Ron con Pasas": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Un sabor para adultos, con el toque de ron y la dulzura de las pasas.",
        "image_url": "/static/images/31.jpeg", "price": "35"
    },
    "Paleta de Cajeta": {
        "type": "Paleta", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un dulce tradicional mexicano en una paleta cremosa. ¡Sabor que enamora!",
        "image_url": "/static/images/32.jpeg", "price": "30"
    },
    "Paleta de Oreo": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "La galleta Oreo en una paleta cremosa. ¡Irresistible!",
        "image_url": "/static/images/33.jpeg", "price": "35"
    },
    "Paleta de Ferrero": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Una paleta gourmet, cremosa y deliciosa, para un gusto muy especial.",
        "image_url": "/static/images/34.jpeg", "price": "45"
    },
    "Paleta de Piñon": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor delicado y único del piñón en una paleta suave.",
        "image_url": "/static/images/35.jpeg", "price": "45"
    },
    "Paleta de Pistache": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Un sabor rico y cremoso que te sorprenderá. Uno de los favoritos.",
        "image_url": "/static/images/36.jpeg", "price": "45"
    },
    "Paleta de Kinder Delice": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "La paleta perfecta para quienes aman el chocolate y la crema. ¡Un postre delicioso!",
        "image_url": "/static/images/37.jpeg", "price": "45"
    },
    "Paleta de Arroz": {
        "type": "Paleta", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "El sabor de un postre tradicional en una paleta cremosa. ¡Inigualable!",
        "image_url": "/static/images/38.jpeg", "price": "30"
    },
    "Paleta de Coco": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El sabor cremoso y tropical del coco en una paleta que te encantará.",
        "image_url": "/static/images/39.jpeg", "price": "35"
    },
    "Paleta de Mazapán": {
        "type": "Paleta", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "El sabor del dulce tradicional en una paleta suave y cremosa.",
        "image_url": "/static/images/40.jpeg", "price": "35"
    },
    "Paleta de Pay de Limón": {
        "type": "Paleta", "base": "Leche", "flavor": ["Cremoso", "Ácido"], "style": "Original",
        "reason": "El postre favorito de muchos, ahora en una paleta. ¡Deliciosamente cremoso y ácido!",
        "image_url": "/static/images/41.jpeg", "price": "35"
    },
    "Paleta de Capuchino": {
        "type": "Paleta", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor del café cremoso en una paleta, ideal para los amantes de esta bebida.",
        "image_url": "/static/images/42.jpeg", "price": "45"
    },
    "Paleta de Zarzamora con Queso": {
        "type": "Paleta", "base": "Leche", "flavor": ["Cremoso", "Dulce"], "style": "Original",
        "reason": "El toque ácido de la zarzamora y lo cremoso del queso se combinan en esta paleta.",
        "image_url": "/static/images/43.jpeg", "price": "35"
    },

    # Aguas
    "Agua de Frutas": {
        "type": "Agua", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Una mezcla de frutas frescas, la bebida perfecta para refrescarse.",
        "image_url": "/static/images/44.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Coco con Nuez": {
        "type": "Agua", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor tropical del coco con el toque crujiente de la nuez. ¡Una delicia refrescante!",
        "image_url": "/static/images/45.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Kahlúa": {
        "type": "Agua", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "Una bebida con sabor a café y un toque cremoso. Perfecta para quienes buscan algo diferente.",
        "image_url": "/static/images/46.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Horchata": {
        "type": "Agua", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un clásico que no puede faltar, dulce y tradicional. ¡Refrescante y deliciosa!",
        "image_url": "/static/images/47.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Piña Colada": {
        "type": "Agua", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Una bebida tropical con un sabor dulce y cremoso. ¡Te sentirás en la playa!",
        "image_url": "/static/images/48.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Fresa": {
        "type": "Agua", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor dulce y refrescante. Perfecta para cualquier momento.",
        "image_url": "/static/images/49.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Limón con Chía": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una opción ligera y ultra-refrescante para quitar la sed.",
        "image_url": "/static/images/50.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Limón con Pepino": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una bebida refrescante y con un toque especial. ¡Ideal para el calor!",
        "image_url": "/static/images/51.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Maracuyá": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Original",
        "reason": "Una bebida exótica con un sabor ácido y refrescante. ¡Te encantará!",
        "image_url": "/static/images/52.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Jamaica": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una bebida tradicional mexicana, floral y ligeramente ácida que refresca al instante.",
        "image_url": "/static/images/53.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Guanábana": {
        "type": "Agua", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Una bebida tropical con un sabor dulce y cremoso. ¡Una delicia!",
        "image_url": "/static/images/54.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Cítricos": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Una mezcla de sabores cítricos para un sabor refrescante y vibrante.",
        "image_url": "/static/images/55.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Tamarindo": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Un sabor agridulce que te recordará a los dulces típicos mexicanos.",
        "image_url": "/static/images/56.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Naranja": {
        "type": "Agua", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "La bebida perfecta para quienes aman el sabor cítrico y refrescante.",
        "image_url": "/static/images/57.jpeg", "price": "25 1/2Lt- 40 Lt"
    },
    "Agua de Naranja con Fresa": {
        "type": "Agua", "base": "Agua", "flavor": ["Ácido", "Dulce"], "style": "Original",
        "reason": "Una combinación de lo ácido de la naranja y lo dulce de la fresa. ¡Una explosión de sabor!",
        "image_url": "/static/images/58.jpeg", "price": "25 1/2Lt- 40 Lt"
    },

    # Helados
    "Helado de Oreo": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor de la galleta Oreo en una textura cremosa. ¡Irresistible!",
        "image_url": "/static/images/59.jpeg", "price": "25-35-45"
    },
    "Helado de Chicle": {
        "type": "Helado", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "Un helado divertido y con un sabor muy original que te recordará a la infancia.",
        "image_url": "/static/images/60.jpeg", "price": "25-35-45"
    },
    "Helado de Fresas con Crema": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El clásico postre mexicano ahora en helado. ¡Una delicia!",
        "image_url": "/static/images/61.jpeg", "price": "25-35-45"
    },
    "Helado de Fresa": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "Un sabor cremoso y suave que nunca falla.",
        "image_url": "/static/images/62.jpeg", "price": "25-35-45"
    },
    "Helado de Beso de Ángel": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Un sabor original y delicioso que te sorprenderá. Cremoso y único.",
        "image_url": "/static/images/63.jpeg", "price": "25-35-45"
    },
    "Helado de Chocolate": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El sabor que nunca falla, perfecto para un momento dulce.",
        "image_url": "/static/images/64.jpeg", "price": "25-35-45"
    },
    "Helado de Vainilla": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "Un sabor suave y dulce que nunca decepciona.",
        "image_url": "/static/images/65.jpeg", "price": "25-35-45"
    },
    "Helado de Queso": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Una opción inusual pero deliciosa, para los que buscan algo diferente.",
        "image_url": "/static/images/66.jpeg", "price": "25-35-45"
    },
    "Helado de Queso con Fresa": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "La combinación perfecta de queso y fresa. ¡Un sabor que te encantará!",
        "image_url": "/static/images/67.jpeg", "price": "25-35-45"
    },
    "Helado de Queso con Zarzamora": {
        "type": "Helado", "base": "Leche", "flavor": ["Cremoso", "Dulce"], "style": "Original",
        "reason": "El contraste perfecto entre el sabor del queso y lo dulce y un poco ácido de la zarzamora.",
        "image_url": "/static/images/68.jpeg", "price": "25-35-45"
    },
    "Helado de Mamey": {
        "type": "Helado", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "Un sabor tropical y cremoso que te transportará a México.",
        "image_url": "/static/images/69.jpeg", "price": "25-35-45"
    },
    "Helado de Piñón": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor delicado y único del piñón en un helado suave.",
        "image_url": "/static/images/70.jpeg", "price": "30-40-50"
    },
    "Helado de Nuez": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "El sabor cremoso y con un toque crujiente de la nuez. ¡Una delicia!",
        "image_url": "/static/images/71.jpeg", "price": "30-40-50"
    },
    "Helado de Ferrero": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "Un helado gourmet, con el sabor del chocolate, la avellana y la crema. ¡Simplemente delicioso!",
        "image_url": "/static/images/72.jpeg", "price": "30-40-50"
    },
    "Helado de Capuchino": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "El sabor del café cremoso en un helado, ideal para los amantes de esta bebida.",
        "image_url": "/static/images/73.jpeg", "price": "45"
    },
    "Helado de Chocomenta": {
        "type": "Helado", "base": "Leche", "flavor": "Cremoso", "style": "Original",
        "reason": "La combinación refrescante de la menta y lo dulce del chocolate.",
        "image_url": "/static/images/74.jpeg", "price": "25-35-45"
    },
    "Helado de Gansito": {
        "type": "Helado", "base": "Leche", "flavor": "Dulce", "style": "Original",
        "reason": "El sabor del pastelito Gansito, ahora en helado. ¡Un gusto que te hará volver a la infancia!",
        "image_url": "/static/images/75.jpeg", "price": "45"
    },
    "Helado de Mango (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un helado ligero y refrescante con el sabor del mango natural.",
        "image_url": "/static/images/76.jpeg", "price": "25-35-45"
    },
    "Helado de Tamarindo (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Un sabor agridulce que te recordará a los dulces típicos mexicanos.",
        "image_url": "/static/images/77.jpeg", "price": "25-35-45"
    },
    "Helado de Limón (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Ácido", "style": "Clásico",
        "reason": "Un helado ligero y ácido, ideal para refrescarse y limpiar el paladar.",
        "image_url": "/static/images/78.jpeg", "price": "25-35-45"
    },
    "Helado de Guanábana (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor exótico y refrescante, ideal para un día de calor.",
        "image_url": "/static/images/79.jpeg", "price": "25-35-45"
    },
    "Helado de Fresa (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "El sabor de fresa en una versión ligera y refrescante.",
        "image_url": "/static/images/80.jpeg", "price": "25-35-45"
    },
    "Helado de Guayaba (agua)": {
        "type": "Helado", "base": "Agua", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un sabor tropical y exótico, ideal para un día de calor.",
        "image_url": "/static/images/81.jpeg", "price": "25-35-45"
    },

    # Especialidades
    "Chamoyadas": {
        "type": "Especialidad", "base": "Agua", "flavor": ["Ácido", "Algo con chile"], "style": "Clásico",
        "reason": "Un postre refrescante y picante, perfecto para el calor.",
        "image_url": "/static/images/82.jpeg" , "price": "35"
    },
    "Fresas con Crema": {
        "type": "Especialidad", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un postre cremoso y dulce, perfecto para compartir o para un gran antojo.",
        "image_url": "/static/images/83.jpeg", "price": "60"
    },
    "Malteadas": {
        "type": "Especialidad", "base": "Leche", "flavor": "Cremoso", "style": "Clásico",
        "reason": "Una opción extra-cremosa para un antojo especial y delicioso.",
        "image_url": "/static/images/84.jpeg", "price": "65"
    },
    "Banana Split": {
        "type": "Especialidad", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un postre clásico con helado, banana, crema batida y chocolate. ¡Para los amantes de lo dulce!",
        "image_url": "/static/images/85.jpeg", "price": "60"
    },
    "Tres Marías": {
        "type": "Especialidad", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Un postre tradicional mexicano, con tres sabores de helado, fruta y crema. ¡Una delicia!",
        "image_url": "/static/images/86.jpeg", "price": "60"
    },
    "Copas de Helado": {
        "type": "Especialidad", "base": "Leche", "flavor": "Dulce", "style": "Clásico",
        "reason": "Elige tus sabores de helado y tus toppings favoritos para crear la copa perfecta.",
        "image_url": "/static/images/87.jpeg", "price": "60"
    },
    "Nachos con Queso": {
        "type": "Especialidad", "base": "N/A", "flavor": "Salado", "style": "Clásico",
        "reason": "Una especialidad salada para variar, deliciosa para disfrutar en un día fresco.",
        "image_url": "/static/images/88.jpeg", "price": "30"
    },
    
}

# Aquí se añade la ruta para servir el index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# ESTA ES LA RUTA CORREGIDA
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/recommend', methods=['POST'])
def recommend_product():
    user_ip = request.remote_addr
    if user_ip == '127.0.0.1':
        user_ip = '8.8.8.8'

    geo_url = f"http://ip-api.com/json/{user_ip}"
    try:
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        city = geo_data.get('city', 'Desconocida')
    except Exception as e:
        print(f"Error en geolocalización: {e}")
        city = "Desconocida"

    temperature = 25
    description = "desconocido"

    if city != "Desconocida":
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
        try:
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            print(f"Clima actual en {city}: {temperature}°C, {description}")
        except requests.exceptions.HTTPError as errh:
            print(f"Error HTTP al obtener el clima: {errh}. La ciudad puede no ser reconocida por la API.")
        except Exception as e:
            print(f"Error al obtener el clima: {e}")

    answers = request.get_json()
    product_type = answers.get('type')
    base = answers.get('base')
    flavor = answers.get('flavor')
    style = answers.get('style')

    scores = {name: 0 for name in products}

    for name, details in products.items():
        if product_type and product_type == details.get('type'):
            scores[name] += 5
        if base and base == details.get('base'):
            scores[name] += 3
        if flavor and (isinstance(details.get('flavor'), list) and flavor in details['flavor'] or flavor == details.get('flavor')):
            scores[name] += 4
        if style and style == details.get('style'):
            scores[name] += 3

        if temperature > 25 and details.get('base') == 'Agua':
            scores[name] += 2
        elif temperature < 15 and details.get('base') == 'Leche':
            scores[name] += 2
        elif temperature < 15 and details.get('type') == 'Especialidad' and (details.get('flavor') == 'Cremoso' or details.get('flavor') == 'Salado'):
            scores[name] += 2

    max_score = max(scores.values())

    best_matches = [name for name, score in scores.items() if score == max_score]

    if best_matches:
        best_match = random.choice(best_matches)
        recommended_product = products[best_match]
    else:
        recommended_product = {
            "product_name": "No pudimos encontrar la recomendación perfecta.",
            "product_price": "??",
            "reason": "Intenta con otras combinaciones.",
            "image_url": "https://via.placeholder.com/250"
        }

    recommendation = {
        "product_name": best_match,
        "product_price": recommended_product["price"],
        "reason": recommended_product["reason"],
        "image_url": recommended_product["image_url"]
    }

    return jsonify(recommendation)

if __name__ == '__main__':
    app.run(debug=True)