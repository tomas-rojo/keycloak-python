* Move env variables away from config

* Make `KeycloakAuthManager` a dependency to be injected after

* Keycloak offers the option to check permissions and policies for different routes, 
so it is possible to remove the @role_required decorator and leave the authorization
logic to Keycloak.

Check more [here](https://youtu.be/RupQWmYhrLA?si=29_mmHcoPB9Y3KuF)
