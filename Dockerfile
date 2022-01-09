FROM bref/php-81-fpm
COPY . /var/task
CMD [ "public/index.php" ]