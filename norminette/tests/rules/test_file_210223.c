int	main(void)
{
	if (pthread_create(&philos[i].philo_status_thread, NULL, \
		check_status, &philos[i]))
		return (-1);
	printf("\nOh noes. I, n°%i, no longer thinks, and therefore, is no more.\
	*dies in philosopher*\n", this->uid);
}
