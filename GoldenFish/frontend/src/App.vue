<template>
    <div id="app">
        <component :is="layout">
            <router-view/>
        </component>
    </div>
</template>

<script>
import EmptyLayout from './layouts/EmptyLayout';
import MainLayout from './layouts/MainLayout'

export default {
    computed: {
        loggedIn() {
            return this.$store.state.auth.status.loggedIn;
        },
        layout() {
            if(this.loggedIn)
                return 'main-layout';
            else
                return 'empty-layout';
        }
    },
    components : {
        EmptyLayout, MainLayout
    }
};
</script>