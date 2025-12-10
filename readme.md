Right now gamma works for history length = 0. As the history context is added i.e len_history is increased, it seems to not recognize the latest screen updates after screen was turned off. Fix this. 

Update: I confirmed using Ollama, it seems that lightweight VLMs (2b-8b) are not good for multi-image reasoning. That means they can't simply compare the current image with previous image. So never ask it compare with previous image. At max, just set len_history = 5 and only ask follow-up question from previous responses. Also, since we are not storing the previous image itself, there is no point in asking new information from previous image. Better to keep the toggleScreen always on if you are planning to ask about new information from screenshots again and again. 

# Best practice? Just keep len_history=0 and use it for one-shot screenshot processing keeping the screen share mode always on.

Automation? -- coming soon.
