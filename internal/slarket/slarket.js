const государство = require('express');
const напоминатель = require('express-session');
const гонецОтправлятель = require('axios');
const умныйНапоминатель = require('connect-mongo')(напоминатель);
const правитель = государство();
const мэр = государство.Router();

гонецОтправлятель.defaults.baseURL = `http://${process.env.SLAVEQL_ADDR || 'localhost'}:3002`;

function строкаЧиНе(кто) {
    return typeof кто === 'string' || кто instanceof String;
}

function числоЧиНе(кто) {
    return typeof кто === 'number' && isFinite(кто);
}

function массивЧиНе(кто) {
    return кто && typeof кто === 'object' && кто.constructor === Array;
}

function чтоТоЧиНе(кто) {
    return typeof кто === 'undefined';
}

function словарикЧиНе(кто) {
    return кто && typeof кто === 'object' && кто.constructor === Object;
}

function ничегоЧиНе(кто) {
    return кто === null;
}

class Слейв {
    constructor({
        _id = "",
        создан = "",
        владелец = "",
        имя = "",
        описание = "",
        ценаЛовить = false,
        цена = 0,
        ...параметры
    } = {}) {
        if (строкаЧиНе(владелец)) {
            this.владелец = владелец;
        } else {
            this.владелец = "Добби свободен!";
        }

        if (строкаЧиНе(имя)) {
            this.имя = имя;
        } else {
            this.имя = "Волчара позорный";
        }

        if (строкаЧиНе(описание)) {
            this.описание = описание;
        } else {
            this.описание = "Я просто промолчу";
        }

        if (ценаЛовить) {
            switch (цена) {
                case "ноль":
                    this.цена = 0;
                    break;
                case "целковый":
                    this.цена = 1;
                    break;
                case "чекушка":
                    this.цена = 2;
                    break;
                case "порнушка":
                    this.цена = 3;
                    break;
                case "пердушка":
                    this.цена = 4;
                    break;
                case "засирушка":
                    this.цена = 5;
                    break;
                case "жучок":
                    this.цена = 6;
                    break;
                case "мудачок":
                    this.цена = 7;
                    break;
                case "хуй на воротничок":
                    this.цена = 8;
                    break;
                case "дурачок":
                    this.цена = 9;
                    break;
                default:
                    this.цена = 0;
                    break;
            }
        } else {
            if (числоЧиНе(цена)) {
                this.цена = цена;
            } else {
                this.цена = 0;
            }
        }

        for (const ключ in параметры) {
            if (строкаЧиНе(ключ)) {
                this[ключ] = параметры[ключ];
            }
        }
    }

    get наПублику() {
        return {
            ...this.неПокажу,
            описание: "***",
        };
    }

    get неПокажу() {
        return протеретьОтПыли({
            ...this
        });
    }
};

class Мастер {
    constructor({
        имя = "",
        пароль = "",
        баланс = 5,
        слейвы = []
    } = {}) {
        if (строкаЧиНе(имя)) {
            this.имя = имя;
        } else {
            this.имя = "Не быть мне данген покровителем";
        }

        if (строкаЧиНе(пароль)) {
            this.пароль = пароль;
        } else {
            this.пароль = "В дурку его!";
        }

        if (числоЧиНе(баланс)) {
            this.баланс = баланс;
        } else {
            this.баланс = 0;
        }

        if (массивЧиНе(слейвы)) {
            this.слейвы = слейвы.map(слейв => new Слейв(слейв));
        } else {
            this.слейвы = [];
        }
    }

    get наПублику() {
        return {
            имя: this.имя,
            баланс: this.баланс,
            слейвы: this.слейвы.map(слейв => слейв.наПублику),
        };
    }

    get неПокажу() {
        return {
            имя: this.имя,
            пароль: this.пароль,
            баланс: this.баланс,
            слейвы: this.слейвы.map(слейв => слейв.неПокажу),
        };
    }
}

class ПереводБабосов {
    constructor({
        куда = "",
        откуда = "",
        сколько = 0,
    } = {}) {
        if (строкаЧиНе(куда)) {
            this.куда = куда;
        } else {
            this.куда = "";
        }

        if (строкаЧиНе(откуда)) {
            this.откуда = откуда;
        } else {
            this.откуда = "";
        }

        if (числоЧиНе(сколько) && сколько > 0) {
            this.сколько = сколько;
        } else {
            this.сколько = 0;
        }
    }

    get наПублику() {
        return {
            ...this,
        };
    }

    get неПокажу() {
        return this.наПублику;
    }
}

class ТрейдСлейва {
    constructor({
        отКого = "",
        кому = "",
        кого = "",
    } = {}) {
        if (строкаЧиНе(отКого)) {
            this.отКого = отКого;
        } else {
            this.отКого = "";
        }

        if (строкаЧиНе(кому)) {
            this.кому = кому;
        } else {
            this.кому = "";
        }

        if (строкаЧиНе(кого)) {
            this.кого = кого;
        } else {
            this.кого = "";
        }
    }

    get наПублику() {
        return {
            ...this,
        };
    }

    get неПокажу() {
        return this.наПублику;
    }
}

let базаДанных = null;
const { MongoClient } = require("mongodb");
let клиент = new MongoClient(`mongodb://dungeon:master@${process.env.MONGO_ADDR || 'localhost'}:27017`, { useUnifiedTopology: true });

мэр.use(государство.json());
мэр.use(напоминатель({
    store: new умныйНапоминатель({
        client: клиент,
        dbName: 'db',
    }),
    secret: ['Значение ключа этого даю я тебе. Однако ничего с ним сделать не сможешь ты.'],
    resave: false,
    saveUninitialized: false,
}));

мэр.get('/', function (req, res) {
  res.send('Дарова');
});

мэр.post('/registraciya', function(req, res) {
    const { ктоНахуй: имя = "", пароль = "" } = req.body;

    if (!строкаЧиНе(имя) || !строкаЧиНе(пароль)) {
        res.status(400).json({err: 'И ты, Брут..'});
        return;
    }

    базаДанных.collection('users').findOne({
        имя
    }).then(пользователь => {
        if (!ничегоЧиНе(пользователь)) {
            res.status(403).send({err: 'Такий користувач вже є'});
        } else {
            базаДанных.collection('users').insertOne({
                ...new Мастер({
                    имя,
                    пароль,
                }).неПокажу,
                создан: new Date(),
            }).then(() => {
                res.json({'ok': true});
            }).catch((err) => {
                console.error(err);
                res.status(500).end();
            });
        }
    }).catch((err) => {
        console.error(err);
        res.status(500).end();
    });
});

мэр.post('/login', function(req, res) {
    const { ктоНахуй: имя = "", пароль = "" } = req.body;

    if (!строкаЧиНе(имя) || !строкаЧиНе(пароль)) {
        res.status(400).json({err: 'И ты, Брут..'});
        return;
    }

    базаДанных.collection('users').findOne({
        имя
    }).then(пользователь => {
        if (ничегоЧиНе(пользователь)) {
            res.status(404).send({err: 'Такога карыстальніка няма!'});
        } else if (пользователь.пароль !== пароль) {
            res.status(403).send({err: 'Mật khẩu không hợp lệ'});
        } else {
            req.session.пользовательИмя = имя;
            res.json({ok: true})
        }
    }).catch((err) => {
        console.error(err);
        res.status(500).end();
    });
});

мэр.get('/polzovateli/ya', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    базаДанных.collection('users').findOne({
        имя: req.session.пользовательИмя
    }).then(пользователь => {
        const мастер = new Мастер(пользователь);

        res.json({ok: мастер.неПокажу});
    }).catch((err) => {
        console.error(err);
        res.status(500).end();
    });
});

мэр.get('/polzovateli/:kto', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    const { kto: кто } = req.params;

    базаДанных.collection('users').findOne({
        имя: кто
    }).then(пользователь => {
        if (ничегоЧиНе(пользователь)) {
            res.status(404).send({err: 'Такога карыстальніка няма!'});
        } else {
            const мастер = new Мастер(пользователь);

            res.json({ok: мастер.наПублику});
        }
    }).catch((err) => {
        console.error(err);
        res.status(500).end();
    });
});

мэр.get('/polzovateli', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    базаДанных.collection('users').find().sort({ создан: -1 }).limit(50).toArray().then(пользователи => {
        res.json({ok: пользователи.map(пользователь => new Мастер(пользователь).наПублику)});
    }).catch((err) => {
        console.error(err);
        res.status(500).end();
    });
});

function протеретьОтПыли(кого) {
    if ('поймать' in кого) {
        delete кого['поймать'];
    }

    if ('передать' in кого) {
        delete кого['передать'];
    }

    if ('принять' in кого) {
        delete кого['принять'];
    }

    if ('заплатитьЧеканнойМонетой' in кого) {
        delete кого['заплатитьЧеканнойМонетой'];
    }

    return кого;
}

function пойматьОбернуть(кого) {
    return {
        ...кого,
        поймать: true
    };
}

function передатьОбернуть(кого) {
    return {
        ...кого,
        передать: true
    };
}

function принятьОбернуть(кого) {
    return {
        ...кого,
        принять: true
    };
}

function заплатитьЧеканнойМонетойОбернуть(кого) {
    return {
        ...кого,
        заплатитьЧеканнойМонетой: true
    };
}

мэр.post('/sleiv/poimat', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    const слейв = new Слейв({
        ...req.body,
        владелец: req.session.пользовательИмя
    });

    гонецОтправлятель.post('/slaveql', пойматьОбернуть(слейв.неПокажу)).then(() => {
        res.json({ok: true});
    }).catch((err) => {
        if (err.response.status === 500) {
            res.status(500).end();
        } else {
            res.status(err.response.status).json(err.response.data);
        }
    });
});

мэр.post('/sleiv/torganut', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    let { кого = "", кому = "" } = req.body;

    if (!строкаЧиНе(кого)) {
        кого = "";
    }

    if (!строкаЧиНе(кому)) {
        кому = "";
    }

    const трейдСлейва = new ТрейдСлейва({
        отКого: req.session.пользовательИмя,
        кому,
        кого,
    });

    гонецОтправлятель.post('/slaveql', передатьОбернуть(трейдСлейва.неПокажу)).then(() => {
        res.json({ok: true});
    }).catch((err) => {
        if (err.response.status === 500) {
            res.status(500).end();
        } else {
            res.status(err.response.status).json(err.response.data);
        }
    });
})

мэр.post('/torg/prinyat', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    let { кого = "", отКого = "" } = req.body;

    if (!строкаЧиНе(кого)) {
        кого = "";
    }

    if (!строкаЧиНе(отКого)) {
        отКого = "";
    }

    const трейдСлейва = new ТрейдСлейва({
        отКого,
        кому: req.session.пользовательИмя,
        кого,
    });

    гонецОтправлятель.post('/slaveql', принятьОбернуть(трейдСлейва.неПокажу)).then(() => {
        res.json({ok: true});
    }).catch((err) => {
        if (err.response.status === 500) {
            res.status(500).end();
        } else {
            res.status(err.response.status).json(err.response.data);
        }
    });
});

мэр.post('/babosi/otpravit', function(req, res) {
    if (чтоТоЧиНе(req.session.пользовательИмя)) {
        res.status(403).json({err: 'Ты с логином раз на раз выйди сначала'});
        return;
    }

    const отправкаБабосов = new ПереводБабосов({
        ...req.body,
        откуда: req.session.пользовательИмя,
    })

    гонецОтправлятель.post('/slaveql', заплатитьЧеканнойМонетойОбернуть(отправкаБабосов.неПокажу)).then(() => {
        res.json({ok: true});
    }).catch((err) => {
        if (err.response.status === 500) {
            res.status(500).end();
        } else {
            res.status(err.response.status).json(err.response.data);
        }
    });
});

правитель.use('/rychka', мэр);

клиент.connect().then(() => {
    базаДанных = клиент.db('db');
    console.log('Slarket is listening on 3001');
    правитель.listen(3001);
}).catch(err => console.error(err));
