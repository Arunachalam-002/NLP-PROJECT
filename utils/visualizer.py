from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(texts, save_path):
    wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(texts))
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
