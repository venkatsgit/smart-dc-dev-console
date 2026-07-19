FROM grafana/grafana:11.5.2

ENV GF_DATE_FORMATS_DEFAULT_TIMEZONE=Asia/Singapore \
    GF_USERS_DEFAULT_THEME=light \
    GF_PATHS_PROVISIONING=/etc/grafana/provisioning \
    GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH=/etc/grafana/dashboards/trends-home.json

COPY grafana/provisioning /etc/grafana/provisioning
COPY grafana/dashboards /etc/grafana/dashboards

EXPOSE 3000
