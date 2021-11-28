import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from cities import Lobby
from cities_list import cities_list
import secret_constanta

vk_session = vk_api.VkApi(token=secret_constanta.TOKEN)
longpoll = VkLongPoll(vk_session)


def is_message(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me


def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})


def get_user_name(user_id):
    user_info = vk_session.method('users.get',
                                  {'user_ids': [user_id]})
    if len(user_info) > 0:
        return user_info[0]['first_name'] + ' ' + user_info[0]['last_name']


def is_start_game(event):
    start_commands = ['играть в города', "хочу играть в города", "города"]
    return event.text.lower() in start_commands


def main():
    players_queue = None
    lobbies = []
    users_in_game = []
    for event in longpoll.listen():
        if is_message(event):
            if event.text == 'привет':
                send_message(event.user_id, 'Привет!')
            elif is_start_game(event):
                if players_queue is None:
                    send_message(event.user_id, 'вы в очереди')
                    players_queue = event.user_id
                elif event.user_id != players_queue:
                    user1 = players_queue
                    user2 = event.user_id
                    lobbies.append(Lobby(user1, user2))
                    users_in_game.extend((user1, user2))
                    players_queue = None
                    send_message(user1, 'Игра началась!')
                    send_message(user2, 'Игра началась!')
                    send_message(lobbies[-1].get_active_player_id(), 'вы ходите первым, наховите город на любую букву')
                elif event.user_id in users_in_game:
                    city = event.text.lower()
                    if city not in cities_list:
                        send_message(event.user_id, 'такого города нет в нашем списке. \n '
                                                    'ты бот')
                        send_message(lobby.get_active_player_id(),"ты победтл")
                        users_in_game.remove(event.user_id)
                        users_in_game.remove(lobby.get_inactive_player_id())
                        lobbies.remove(lobby)

                        continue
                    lobby = find_lobby(lobbies, event.user_id)
                    if not lobby.is_correct_letter(city[0]):
                        send_message(event.user_id, 'ты бот учи геаграфию')
                        continue
                    if lobby.get_active_player_id() == event.user_id:
                        send_message(event.user_id, ['сейчас не твой ход бот'])
                        continue
                    lobby.change_last_letter(city)
                    lobby.used_cities.append(city)
                    lobby.change_current_turn()
                    send_message(lobby.get_active_player_id(),f'вам на букву:{lobby.last_letter}\n'
                                                              f'Игрок назвал город:{city}')


def find_lobby(lobbies, user_id):
    for lobby in lobbies:
        if user_id in lobby.user_ids:
            return lobby



main()
