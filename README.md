Add a simple compiler & interpreter for your slack
==================================================

Disclaimer: This implementation is not very safe. Run it with only good people. At least run it on isolated and not very important servers.


Install
-------

    pip install -r requirements.txt


Run
---

This is a WSGI app. You can demonize it with gunicorn or other similar tools.

In easier way:


   ./manage.py runserver 0.0.0.0 <port>


In this case, it is not demonized. Run it in screen or tmux.


Languages
---------

See: https://github.com/youknowone/slackcode/blob/master/engine.py#L210

Interpreters or compilers must be installed and accessible in PATH.


Example
-------

    !save rot13 !py print string.translate('''{{:}}''', string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"))

    > !!rot13 Hello, World!
    < Uryyb, Jbeyq!
    > !!rot13 Uryyb, Jbeyq!
    < Hello, World!


    !save 밯망희 !아희 밯망희

    > !!밯망희 헬
    < 54764


    !save 날씨 !py r = requests.get('http:' + '//www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1141058500'); s = bs4.BeautifulSoup(r.text).find('data'); x = u'{}시 기온: {} 기상: {} 풍향: {}'.format(s.find('hour').text, s.find('temp').text, s.find('wfkor').text, s.find('wdkor').text); print x.encode('utf-8')

    > !!날씨
    < (diverse for every running)

