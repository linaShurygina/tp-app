<template>
  <div class="container">
    <div class="site-title">
            <span class="site-name">Golden Fish</span>
            <img src="../assets/img/christmas-decoration.png" class="cristmas-decoration">
        </div>

    <form name="form" @submit.prevent="handleRegister">
        <div>
          <span v-if="message" class="error">{{message}}</span>
        </div>

      <input
        v-model="user.email"
        type="email"
        name="email"
        placeholder="Email *"
        autocomplete="off"
      />

      <input
        v-model="user.username"
        type="text"
        name="username"
        placeholder="Юзернейм *"
        autocomplete="off"
      />

      <input
        v-model="user.name"
        type="text"
        name="name"
        placeholder="Имя *"
        autocomplete="off"
      />

      <input
        v-model="user.surname"
        type="text"
        name="surname"
        placeholder="Фамилия *"
        autocomplete="off"
      />

      <input
        v-model="user.password"
        type="password"
        name="password"
        placeholder="Пароль *"
      />

      <input
        v-model="user.birthday"
        type="date"
        name="birtday"
      />

      <input
        type="submit"
        value="Зарегистрироваться"
        class="button"
      />

    </form>
  </div>
</template>

<script>
import User from '../models/user';

export default {
    name: 'Register',
    data() {
        return {
            user: new User(),
            submitted: false,
            successful: false,
            message: ''
        };
    },
    computed: {
        loggedIn() {
            return this.$store.state.auth.status.loggedIn;
        }
    },
    mounted() {
        document.title = "Регистрация";
        if (this.loggedIn) {
            this.$router.push('/mywishes');
        }
    },
    methods: {
        handleRegister() {
            this.message = '';
            this.submitted = true;
            if (this.isFormValid()) {
                this.$store.dispatch('auth/register', this.user).then(
                () => {
                    this.$router.push('/mywishes');
                },
                error => {
                    console.log(error.message);
                    this.message = 'Email и/или юзернейм уже существует';
                    this.successful = false;
                }
            );
        }
        },
        isFormValid() {
            if(this.user.email === '' || this.user.password === '' || 
            this.user.username === '' || this.user.name === '' ||
            this.user.surname === '') {
                this.message = 'Не все обязательные поля заполенены';
                return false;
            }  
            else if(!this.isEmailValid() || !this.isUsernameValid() || !this.isNameValid() || 
            !this.isSurnameValid() || !this.isPasswordValid()) {
                return false;
            }
            else
                return true;             
        },
        isEmailValid() {
            const email = this.user.email;
            const regexp = RegExp('.@.');
            if(!regexp.test(email)) {
                this.message = 'Некорректный email';
                return false;
            }
            else
                return true;
        },
        isUsernameValid() {
            const username = this.user.username;
            const regexp = RegExp('^[^a-zA-Zа-яА-Я]');
            if(username.length < 3 || regexp.test(username)) {
                this.message = 'Юзернейм должен содержать минимум 3 символа и не начинаться с цифры или специального символа';
                return false;
            }
            else
                return true;
        },
        isNameValid() {
            const name = this.user.name;
            const regexp = RegExp('[^a-zA-Zа-яА-Я]');
            if(name.length < 2 || regexp.test(name)) {
                this.message = 'Имя должно содержать минимум 2 символа и состоять из символов латинского или русского алфавита';
                return false;
            }
            else
                return true;
        },
        isSurnameValid() {
            const surname = this.user.surname;
            const regexp = RegExp('[^a-zA-Zа-яА-Я]');
            if(surname.length < 2 || regexp.test(surname)) {
                this.message = 'Фамилия должна содержать минимум 2 символа и состоять из символов латинского или русского алфавита';
                return false;
            }
            else
                return true;
        },
        isPasswordValid() {
            const password = this.user.password;
            if(password.length < 5) {
                this.message = 'Пароль должен содержать минимум 5 символов';
                return false;
            }
            else
                return true;
        }
    }
};
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Ovo);
@import url(https://fonts.googleapis.com/css?family=Poiret+One);

.site-title {
    display: flex;
    flex-direction: column;
}

.site-name {
    height: 54px;
    font-family: "Ovo";
    font-size: 48px;
    line-height: 54px;
    color: #D8B661;
    text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.cristmas-decoration {
    width: 250px;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

form * {
    margin-top: 34px;
}

input {
    background-color: #6C3F5E;
    width: 315px;
    border: 0;
    border-bottom: 1px solid #A88F8F;
    color: #A88F8F;
}

input::-webkit-input-placeholder { 
    color: #A88F8F;
}

.button {
    width: 194px;
    height: 31px;
    background: #C6A960;
    font-family: Poiret One;
    font-size: 20px;
    line-height: 23px;
    text-align: center;
    color: #000000;
    border: 0;
}

.button:hover {
    font-weight: bold;
}

.error {
    font-family: Poiret One;
    text-align: center;
    font-size: 20px;
    line-height: 23px;
    font-style: normal;
    font-weight: bold;
    color: #000000;
}
</style>