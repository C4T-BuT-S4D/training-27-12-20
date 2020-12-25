const государство = require('express');
const правитель = государство();

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

        if (числоЧиНе(цена)) {
            this.цена = цена;
        } else {
            this.цена = 0;
        }

        for (const ключ in параметры) {
            if (строкаЧиНе(ключ)) {
                this[ключ] = параметры[ключ];
            }
        }
    }

    get наПублику() {
        return {
            ...this,
            описание: "***",
        };
    }

    get неПокажу() {
        return {
            ...this
        }
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

правитель.use(государство.json());

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

правитель.post('/slaveql', function (req, res) {
    if (req.body.заплатитьЧеканнойМонетой) {
        const переводБабосов = new ПереводБабосов(протеретьОтПыли(req.body));
        базаДанных.collection('users').findOne({
            имя: переводБабосов.откуда
        }).then(пользователь => {
            const мастер = new Мастер(пользователь);
            if (мастер.баланс < переводБабосов.сколько) {
                res.status(403).json({err: 'ДЕНЕГ НЕТ, НО ВЫ ДЕРЖИТЕСЬ'})
            } else {
                базаДанных.collection('users').updateOne({
                    имя: переводБабосов.откуда
                }, {
                    '$inc': {
                        баланс: -переводБабосов.сколько
                    }
                }).then(() => {
                    базаДанных.collection('users').updateOne({
                        имя: переводБабосов.куда
                    }, {
                        '$inc': {
                            баланс: переводБабосов.сколько
                        }
                    }).then(() => {
                        res.json({ok: true});
                    }).catch((err) => {
                        console.error(err);
                        res.status(500).end();
                    });
                }).catch((err) => {
                    console.error(err);
                    res.status(500).end();
                });
            }
        }).catch((err) => {
            console.error(err);
            res.status(500).end();
        });
    }

    if (req.body.принять) {
        const трейдСлейва = new ТрейдСлейва(протеретьОтПыли(req.body));

        базаДанных.collection('trades').findOne(трейдСлейва).then(поссиблТрейд => {
            if (ничегоЧиНе(поссиблТрейд)) {
                res.status(403).json({err: 'Короче, Меченый, я тебя спас и в благородство играть не буду: выполнишь для меня пару заданий — и мы в расчете'});
            } else {
                базаДанных.collection('users').findOne({
                    имя: трейдСлейва.кому
                }).then(пользователь => {
                    const кому = new Мастер(пользователь);
                    базаДанных.collection('users').findOne({
                        имя: трейдСлейва.отКого
                    }).then(пользователь => {
                        const мастер = new Мастер(пользователь);
                        const слейв = мастер.слейвы.filter(слейв => слейв.имя === трейдСлейва.кого)[0];
                        if (слейв.цена > кому.баланс) {
                            res.status(403).json({err: 'Налево пойдешь - целковый найдешь'});
                        } else {
                            базаДанных.collection('users').updateOne({
                                имя: кому.имя,
                            }, {
                                '$set': {
                                    слейвы: кому.слейвы.concat([слейв])
                                },
                                '$inc': {
                                    баланс: -слейв.цена
                                }
                            }).then(() => {
                                базаДанных.collection('users').updateOne({
                                    имя: мастер.имя
                                }, {
                                    '$inc': {
                                        баланс: слейв.цена
                                    }
                                }).then(() => {
                                    res.json({ok: true});
                                }).catch((err) => {
                                    console.error(err);
                                    res.status(500).end();
                                });
                            }).catch((err) => {
                                console.error(err);
                                res.status(500).end();
                            });
                        }
                    }).catch((err) => {
                        console.error(err);
                        res.status(500).end();
                    });
                }).catch((err) => {
                    console.error(err);
                    res.status(500).end();
                });
            }
        }).catch((err) => {
            console.error(err);
            res.status(500).end();
        });
    }

    if (req.body.передать) {
        const трейдСлейва = new ТрейдСлейва(протеретьОтПыли(req.body));

        базаДанных.collection('users').findOne({
            имя: трейдСлейва.отКого
        }).then(пользователь => {
            const мастер = new Мастер(пользователь);

            if (мастер.слейвы.filter(слейв => слейв.имя === трейдСлейва.кого).length > 0) {
                базаДанных.collection('trades').insertOne(трейдСлейва);
                res.json({ok: true})
            } else {
                res.status(404).json({err: 'Такого слейва нема'});
            }
        }).catch((err) => {
            console.error(err);
            res.status(500).end();
        });
    }

    if (req.body.поймать) {
        const слейв = new Слейв(протеретьОтПыли(req.body));
        базаДанных.collection('users').findOne({
            имя: слейв.владелец
        }).then(пользователь => {
            базаДанных.collection('users').updateOne({
                имя: слейв.владелец
            }, {
                '$set': {
                    слейвы: пользователь.слейвы.concat([слейв])
                }
            }).then(() => {
                res.json({ok: true});
            }).catch((err) => {
                console.error(err);
                res.status(500).end();
            });
        }).catch((err) => {
            console.error(err);
            res.status(500).end();
        });
    }
});

клиент.connect().then(() => {
    базаДанных = клиент.db('db');
    console.log('Slaveql is listening on 3002');
    правитель.listen(3002);
}).catch(err => console.error(err));
