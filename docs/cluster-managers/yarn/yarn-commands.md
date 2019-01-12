# YARN Commands

```
yarn application -appStates FINISHED -list | grep ${APP_NAME} | head -n 1 | awk -F' ' '{print $1}' | xargs yarn application -status
```