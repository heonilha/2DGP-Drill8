def event_to_string(state_event):
    from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
    import pico2d

    event_names = {
        SDL_KEYDOWN: 'KEYDOWN',
        SDL_KEYUP: 'KEYUP',
        SDL_MOUSEMOTION: 'MOUSEMOTION',
        SDL_MOUSEBUTTONDOWN: 'MOUSEBUTTONDOWN',
        SDL_MOUSEBUTTONUP: 'MOUSEBUTTONUP'
    }
    state_event_type = state_event[0]
    event = state_event[1]
    if state_event_type != 'INPUT':
        return f"{state_event}"

    key_names = {}
    for name in dir(pico2d):
        if name.startswith('SDLK_'):
            key_code = getattr(pico2d, name)
            key_name = name.replace('SDLK_', '')
            key_names[key_code] = key_name

    event_type = event_names.get(event.type, f'Unknown({event.type})')
    key_name = key_names.get(event.key, f'key({event.key})')

    info = f'{event_type}:{key_name}'

    if event.type in (SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
        info += f', pos=({event.x},{event.y})'

    if event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
        info += f', button={event.button}'

    if hasattr(event, 'mod') and event.mod:
        info += f', mod={event.mod}'

    return f"('{state_event_type}', {info})"