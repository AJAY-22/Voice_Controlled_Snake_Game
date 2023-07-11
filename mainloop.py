import numpy as np

from tensorflow.keras import models

from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer

# !! Modify this in the correct order
commands = ['left', 'down', 'stop', 'up', 'right', 'no', 'go', 'yes']
commands = ['down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']
loaded_model = models.load_model("saved_model")
# something
def predict_mic():
    audio = record_audio()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    max_val = np.max(prediction)
    label_pred = [3]
    if max_val > 0:
        label_pred = np.argmax(prediction, axis=1)
    
    command = commands[label_pred[0]]
    print("Predicted label:", command)
    return command
seconds_to_wait = 2
if __name__ == "__main__":
    from game import SnakeGameAI, Direction, Point
    import time
    game = SnakeGameAI()
    while True:
        time.sleep(seconds_to_wait)
        print("SPEAK")
        command = predict_mic()
        # final_move = [RIGHT, DOWN, LEFT, UP]
        final_move = [0, 0, 0, 0]
        if command == "right":
            final_move = [1, 0, 0, 0]
        if command == "down":
            final_move = [0, 1, 0, 0]
        if command == "left":
            final_move = [0, 0, 1, 0]
        if command == "up":
            final_move = [0, 0, 0, 1]
        
        _, gameover, _ = game.play_step(final_move)
        
        if gameover:
            game.reset()
        if command == "stop":
            game.quit()
            terminate()
            break