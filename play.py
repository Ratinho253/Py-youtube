from logging import error
from pytube import YouTube, Playlist  # Importa Playlist para suportar downloads de playlists
import yt_dlp
from tkinter import *
import tkinter.messagebox as tkMessageBox
import os
from tkinter import ttk

def selecionado(event, textnome):
    """Função para apagar o texto padrão quando o campo é selecionado."""
    textnome.delete(0, 'end')
    textnome.config(fg='black')

def deselecionado(event, textnome):
    """Função para reexibir o texto padrão caso o campo esteja vazio."""
    if textnome.get() == "":
        textnome.insert(0, '**Site obrigatório!')
        textnome.config(fg='red')

def saindo():
    """Função para confirmar a saída da aplicação."""
    result = tkMessageBox.askquestion("", "Confirma a saída?", icon='question')
    if result == 'yes':
        os._exit(1)

def limpar():
    """Limpa o campo de link e reseta a barra de progresso."""
    txtLink.delete(0, "end")
    progress1.stop()

def baixadormp3():
    """Baixa vídeo ou playlist em formato MP3."""
    progress1['value'] += 10  # Atualiza barra de progresso
    tela.update()
    video_url = txtLink.get()
    txtLink['state'] = DISABLED

    try:
        # Verifica se o link é de uma playlist
        if 'playlist' in video_url:
            playlist = Playlist(video_url)
            tkMessageBox.showinfo("Playlist", message=f"Iniciando download da playlist: {playlist.title}")
            caminhosalvar = r"D:\dowload\Nova pasta\casamento"  # Caminho fixo
            os.makedirs(caminhosalvar, exist_ok=True)
            
            # Itera pelos vídeos da playlist
            for url in playlist.video_urls:
                video_info = yt_dlp.YoutubeDL().extract_info(url=url, download=False)
                filename = f"{video_info['title']}.mp3"
                options = {
                    'format': 'bestaudio/best',
                    'keepvideo': False,
                    'outtmpl': os.path.join(caminhosalvar, filename)
                }
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
        else:
            # Caso seja um único vídeo
            video_info = yt_dlp.YoutubeDL().extract_info(url=video_url, download=False)
            filename = f"{video_info['title']}.mp3"
            caminhosalvar = r"D:\dowload\Nova pasta\casamento"
            os.makedirs(caminhosalvar, exist_ok=True)
            options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'outtmpl': os.path.join(caminhosalvar, filename)
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_url])

        txtLink['state'] = NORMAL
        tkMessageBox.showinfo("Download complete", message="Finalizado! Verifique em: " + str(caminhosalvar))
        limpar()
    except Exception as e:
        progress1.stop()
        txtLink['state'] = NORMAL
        tkMessageBox.showinfo("Erro", message=f"Não foi possível finalizar!!\n{e}")

def baixadormp4():
    """Baixa vídeo ou playlist em formato MP4."""
    site = txtLink.get()
    txtLink['state'] = DISABLED
    progress1['value'] += 10
    tela.update()
    try:
        # Verifica se o link é de uma playlist
        if 'playlist' in site:
            playlist = Playlist(site)
            tkMessageBox.showinfo("Playlist", message=f"Iniciando download da playlist: {playlist.title}")
            caminhosalvar = r"C:\Downloads\MP4"
            os.makedirs(caminhosalvar, exist_ok=True)
            
            for url in playlist.video_urls:
                tube = YouTube(url)
                tube.streams.get_highest_resolution().download(caminhosalvar)
        else:
            # Caso seja um único vídeo
            tube = YouTube(site)
            progress1['value'] += 10
            tela.update()

            tubes = tube.streams.get_highest_resolution()
            progress1['value'] += 10
            tela.update()

            caminhosalvar = r"C:\Downloads\MP4"  # Caminho fixo para salvar os arquivos
            os.makedirs(caminhosalvar, exist_ok=True)
            tubes.download(caminhosalvar)

        txtLink['state'] = NORMAL
        tkMessageBox.showinfo("Finalizado", message="Finalizado! Verifique em: " + str(caminhosalvar))
        limpar()
    except Exception as e:
        progress1.stop()
        txtLink['state'] = NORMAL
        tkMessageBox.showinfo("Erro", message=f"Não foi possível finalizar!!\n{e}")

def progresso(escolhido):
    """Inicia o processo de download com base no formato escolhido."""
    site = txtLink.get()
    if site == "" or site == '**Site obrigatório!' or site == 'Site':
        tkMessageBox.showinfo("Erro", message="Favor preencher o site!!")
    else:
        if escolhido == "mp4":
            progress1.start(10)
            baixadormp4()
        else:
            progress1.start(10)
            baixadormp3()

# Configurações da tela principal
tela = Tk()
tela.title("Download De Videos MP4 e MP3")
tela.geometry("800x500+400+0")
tela['bg'] = "OrangeRed"

# Substitua por um ícone válido ou comente a linha se o arquivo não existir
tela.iconphoto(True, PhotoImage(file='./arquivos/foto.png'))

image = PhotoImage(file='./arquivos/foto2.png')
campointervalo = Label(tela, width=800, height=500, image=image, bd=3, fg='black', bg='black', font=('arial', 10, 'bold'))
campointervalo.grid(rowspan=10, columnspan=5)

lblLink = Label(tela, bg="DarkOrange", text="**Site: ", font=('arial', 14, 'bold'))
lblLink.place(relx=0.2, rely=0.2)

# Entrada de texto
txtLink = Entry(tela, justify='center', fg='red', font=('arial', 14, 'bold'))
txtLink.place(relx=0.3, rely=0.2)
txtLink.insert(0, 'Site')
txtLink.bind('<FocusIn>', lambda event=txtLink, btn=txtLink: selecionado(event, btn))
txtLink.bind('<FocusOut>', lambda event=txtLink, btn=txtLink: deselecionado(event, btn))

# Botões principais
btinicio = Button(tela, text=" Baixar MP4  ", bg="DarkOrange", font=('arial', 14, 'bold'), command=lambda: progresso('mp4'))
btinicio.place(relx=0.1, rely=0.8)

btimusica = Button(tela, text=" Baixar MP3  ", bg="DarkOrange", font=('arial', 14, 'bold'), command=lambda: progresso('mp3'))
btimusica.place(relx=0.3, rely=0.8)

btilimpa = Button(tela, text=" Limpar  ", bg="DarkOrange", font=('arial', 14, 'bold'), command=limpar)
btilimpa.place(relx=0.5, rely=0.8)

btsair = Button(tela, text="   Sair   ", bg="DarkOrange", font=('arial', 14, 'bold'), command=saindo)
btsair.place(relx=0.65, rely=0.8)

# Progress bar
s = ttk.Style()
s.theme_use('default')
s.configure("SKyBlue1.Horizontal.TProgressbar", foreground='red', background='red')

progress1 = ttk.Progressbar(tela, orient=VERTICAL, length=450, style="SKyBlue1.Horizontal.TProgressbar", mode='determinate')
progress1.place(relx=0.005, rely=0)

tela.mainloop()
