<script setup>
import User from '../components/User.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Castle IQ</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <!-- <li class="nav-item">
                        <RouterLink class="nav-link active" to="/">Home</RouterLink>
                    </li> -->
                    <!-- <li class="nav-item">
                        <RouterLink class="nav-link active" to="/users">Користувачі</RouterLink>
                    </li> -->
                    <li class="nav-item">
                        <a href="#" class="nav-link disabled">Користувачі</a>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link active" to="/devices">Пристрої</RouterLink>
                    </li>
                    <li class="nav-item">
                        <a href="#" class="nav-link disabled">Автоматизації</a>
                    </li>
                    <!-- <li class="nav-item">
                        <RouterLink class="nav-link active" to="/about">About</RouterLink>
                    </li>
                    <li class="nav-item">
                        <RouterLink class="nav-link active" to="/test">Test</RouterLink>
                    </li> -->
                    <!-- <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Dropdown
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li> -->
                    <!-- <li class="nav-item">
                        <a class="nav-link disabled">Disabled</a>
                    </li> -->
                </ul>
                <form class="d-flex" role="search">
                    <User />
                </form>
            </div>
        </div>
    </nav>
</template>