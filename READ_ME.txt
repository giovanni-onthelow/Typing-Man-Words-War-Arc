Background dari game
Dunia sudah di ambang akhir, matahari telah hilang dan yang terlihat di bumi ini hanyalah kegelapan malam.
War devil telah mengeluarkan sebuah devil dari neraka yang menjadi mimpi buruk bagi manusia, yaitu WORD DEVIL.

Hanya satu orang lah yang bisa melindungi umat manusia yang tersisa dari devil ini, yaitu TYPING MAN.
Dengan bantuan dari gun devil dan fire devil, ia menggunakan sebuah senjata yang mengeluarkan peluru api untuk menaklukkan
word devil dan menjaga sisa sisa dari umat manusia.

SEBELUM MULAI
Pastikan kalian sudah menginstall NLTK (Natural Language Toolkit)
1. Install melalui terminal atau command prompt.
    pip install nltk
    *Jika kamu menggunakan PyCharm, kamu juga bisa menginstalnya melalui
    menu Settings > Project: [NamaProyek] > Python Interpreter.
2. Setelah itu masukkan kode dibawah ini dalam proyek atau di file python baru
    import nltk
    # Mengunduh korpus kata-kata bahasa Inggris
    nltk.download('words')
3. Setelah terinstal dan terunduh, kamu bisa memanggil daftar kata
    tersebut di dalam proyekmu seperti ini:
    from nltk.corpus import words
    # Mengambil semua kata dalam bahasa Inggris
    word_list = words.words()

Tipe-tipe musuh:
    1. Word Biasa : Biasa memiliki jumlah huruf yang tergantung dengan pilihan "letters",
    kalau tidak di input akan mengurangi 1 Lives (nyawa). Memiliki warna huruf putih.

    2. Word Bomb : Jika di input maka lives (nyawa) akan berkurang 2,
    jika tidak di input tidak akan mengurangi nyawa. Memiliki warna huruf oranye.

    3. Word Boss : Jika di input maka lives (nyawa) akan bertambah 2,
    jika tidak di input maka nyawa akan berkurang 1. Memiliki warna huruf merah.
