import random
from flask import Blueprint, request, jsonify

destiny_bp = Blueprint('template', __name__)

def read_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [word.strip() for word in f]
#Title = ["o Furry", "O Eterno", "o rei", "o nazista", "o especialista", "o feiticeiro", "o professor", "o lendário", "o destemido", "o temido", " o presidente", "o monge", "o Deus", "Moon", "o vigarista", "o pai de", "o shinigami", "o soldado", "o capitão", "o herói", "o pirata", "o demônio"];
#var Name = [message.member.user.username , "Harley", "Pancake", "Wasabi", "Danyel", "Carlos", "Komasan", "Mike Azarel",  "Misterlock", "Judy Hopps", "Dogguinhas ", "Stuff", "Tastes", "Femboy Dogguinhas", "JellyBean", "Sethzerr", "Boingo", "Lars Moon", "Shira Zem", "Smokey Brown", "Isabelle", "Ciel", "Nick Wilde", "Rupninja Trash", "Siggy", "Corgi", "Ninja", "Moon", "Gui", "Jasper", "King Sparda", "Hitler", "Anonimo", "Raposa", "Roki'z", "Potter", "Cassie", "Kratos", "Buddha", "FURINHAS", "SRF", "SnexMy", "Zuko Vyper"];
#var Class = ["Artista", "Dinossauro", "Otaku", "Advogado", "Escolhido", "Furry", "Cavaleiro", "Servente", "Judeu", "Mago", "Ladino", "Sílfide", "Vidente", "Ladrão", "Herdeiro", "Bardo", "Princípe", "Bruxo", "Mestre", "Templário", "Médico", "Salada", "Lobo", "Dragão", "Unicórnio", "Canadense"];
#var Aspect = ["do Yiff", "de Sangue", "do Tempo", "do Vento", "da Destruição", "do Coração", "do Espaço", "da Mente", "da Luz", "do Vazio", "da Fúria", "da Paz", "da Vida", "dos Magos", "do Apocalipse", "das trevas", "do caos", "do submundo", "de Oblivion" ,"da chuva", "do fogo"];
#var Verbo = ["yiffar", "questionar", "penetrar", "estudar", "confinar", "lutar com", "dormir com", "morrer para", "cursar", "zoar", "casar-se com", "escravizar", "acabar com", "libertar", "derrotar", "guiar", "criar", "vender", "destruir", "abduzir", "explodir", "se comunicar com", "explorar", "fundar", "conquistar", "desbravar", "filosofar sobre", "comer", "guerrear com", "perfurar", "flertar com"];
#var Destino = ["açaí", "Sonic", "area 51", "Daft Punk", "Brazilian Furry Memes", "waifu", "seus próprios sentimentos", "memes", "a irmazinha", "nada", "o JoJo", "você mesmo", "Brasil", "Russia", "dois furries ao mesmo tempo", "a Internet", "OCs", "Telephone", "Majira Strawberry", "FurAffinity", "o Curso", "Amino Furry", "Yiff", "Minecraft", "Planeta Furry", "OwO", "os Furries", "os Boingos", "o YouTube", "os escravos", "Crash Azarel", "a FBI", "Kronos", "os negros", "a América", "o Reino Unido", "sua mãe", "os sete mares", "os Deuses", "um sanduiche", "o Kraken", "o mundo", "o futuro", "Leviathan", "os alienígenas", "os céus", "os brancos", "os veganos", "os animes", "Dorime"]
        
names = read_words('destiny/names.txt')
titles = read_words('destiny/titles.txt')
aspects = read_words('destiny/aspect.txt')
Classes = read_words('destiny/class.txt')
destinies = read_words('destiny/destinies.txt')
destinations = read_words('destiny/destinations.txt')

@destiny_bp.route('/api/destiny', methods=['GET', 'POST'])
def generate_text():
    name = random.choice(names)
    title = random.choice(titles)
    aspect = random.choice(aspects)
    Class = random.choice(Classes)
    destiny = random.choice(destinies)
    destination = random.choice(destinations)

    text = f"Você é {title} {name}, O {Class} {aspect}, destinado a {destiny} {destination}!"
    return jsonify({'text': text})
