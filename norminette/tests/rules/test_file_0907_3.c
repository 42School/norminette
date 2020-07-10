int		main(int argc, char *argv[])
{
	int				cc;
	struct termios 	rtt, stt;
	struct winsize	win;
	struct timeval	tv, *tvp;
	time_t			tvec, start;
	char			obuf[BUFSIZ];
	char			ibuf[BUFSIZ];
	fd_set			rfd;
	int				aflg, Fflg, kflg, pflg, ch, k, n;
	int				flushtime, readstdin;
	int				fm_fd, fm_log;

	aflg = Fflg = kflg = pflg = 0;
	usesleep = 1;
	rawout = 0;
	flushtime = 30;
	fm_fd = -1;	/* Shut up stupid "may be used uninitialized" GCC
				warning. (not needed w/clang) */
	showexit = 0;

	while ((ch = getopt(argc, argv, "adFkpqrt:")) != -1)
		switch(ch) {
			case 'a':
				aflg = 1;
				break;
			case 'd':
				usesleep = 0;
				break;
			case 'F':
				Fflg = 1;
				break;
			case 'k':
				kflg = 1;
				break;
			case 'p':
				pflg = 1;
				break;
			case 'q':
				qflg = 1;
				break;
			case 'r':
				rawout = 1;
				break;
			case 't':
				flushtime = ft_atoi(optarg);
				if (flushtime < 0)
					ft_err(1, "invalid flush time");
				break;
			case '?':
			default:
				usage();
		}
	argc -= optind;
	argv += optind;

	if (argc > 0)
	{
		fname = argv[0];
		argv++;
		argc--;
	} else
		fname = "typescript";
	int		flopen = pflg ? O_RDONLY : aflg ? O_CREAT|O_RDWR|O_APPEND : O_CREAT|O_RDWR|O_TRUNC;
	if ((fdscript = open(fname, flopen, OPEN_MODE)) == -1)
		ft_err(1, fname);

	/*if (pflg)
		playback(fscript);*/

	if ((ttyflg = pty_isatty(STDIN_FILENO)) != 0) {
		if (ioctl(STDIN_FILENO, TIOCGETA, &tt) == -1)
			ft_err(1, "tcgetattr");
		if (ioctl(STDIN_FILENO, TIOCGWINSZ, &win) == -1)
			ft_err(1, "ioctl");
		if (pty_open(&master, &slave, NULL, &tt, &win) == -1)
			ft_err(1, "openpty");
	} else {
		if (pty_open(&master, &slave, NULL, NULL, NULL) == -1)
			ft_err(1, "openpty");
	}

	if (rawout)
		record(fdscript, NULL, 0, 's');

	if (!qflg)
	{
		tvec = time(NULL);
		(void)ft_putstr("Script started, output file is ");
		(void)ft_putendl(fname);
		// (void)printf("Script started, output file is %s\n", fname);
		if (!rawout) {
			(void)ft_putstr_fd("Script started on ", fdscript);
			(void)ft_putstr_fd(ctime(&tvec), fdscript);
			// (void)fprintf(fscript, "Script started on %s", ctime(&tvec));
			if (argv[0]) {
				showexit = 1;
				(void)ft_putstr_fd("Command:", fdscript);
				for (k = 0 ; argv[k] ; ++k) {
					(void)ft_putstr_fd(" ", fdscript);
					(void)ft_putstr_fd(argv[k], fdscript);
				}
				(void)ft_putstr_fd("\n", fdscript);
			}
		}
		fsync(fdscript);
	}
	if (ttyflg)
	{
		rtt = tt;
		pty_cfmakeraw(&rtt);
		rtt.c_lflag &= ~ECHO;
		(void)ioctl(STDIN_FILENO, TIOCSETAF, &rtt);
	}

	child = fork();
	if (child < 0) {
		(void)ft_putstr_fd("fork", STDERR_FILENO);
		done(1);
	}
	if (child == 0)
	{
		doshell(argv);
	}
	close(slave);

	start = tvec = time(0);
	readstdin = 1;
	while (42)
	{
		FD_ZERO(&rfd);
		FD_SET(master, &rfd);
		if (readstdin)
			FD_SET(STDIN_FILENO, &rfd);
		if (!readstdin && ttyflg)
		{
			tv.tv_sec = 1;
			tv.tv_usec = 0;
			tvp = &tv;
			readstdin = 1;
		}
		else if (flushtime > 0)
		{
			tv.tv_sec = flushtime - (tvec - start);
			tv.tv_usec = 0;
			tvp = &tv;
		}
		else
		{
			tvp = NULL;
		}
		n = select(master + 1, &rfd, 0, 0, tvp);
		if (n < 0 && errno != EINTR)
			break;
		if (n > 0 && FD_ISSET(STDIN_FILENO, &rfd)) {
			cc = read(STDIN_FILENO, ibuf, BUFSIZ);
			if (cc < 0)
				break;
			if (cc == 0)
			{
				if (ioctl(STDIN_FILENO, TIOCGETA, &stt) == 0 && (stt.c_lflag & ICANON) != 0)
				{
					(void)write(master, &stt.c_cc[VEOF], 1);
				}
				readstdin = 0;
			}
			if (cc > 0) {
				if (rawout)
					record(fdscript, ibuf, cc, 'i');
				(void)write(master, ibuf, cc);
				if (kflg && ioctl(STDIN_FILENO, TIOCGETA, &stt) >= 0 && ((stt.c_lflag & ECHO) == 0))
				{
					(void)write(fdscript, ibuf, cc);
				}
			}
		}
		if (n > 0 && FD_ISSET(master, &rfd))
		{
			cc = read(master, obuf, sizeof (obuf));
			if (cc <= 0)
				break;
			(void)write(STDOUT_FILENO, obuf, cc);
			if (rawout)
				record(fdscript, obuf, cc, 'o');
			else
				(void)write(fdscript, obuf, cc);
		}
		tvec = time(0);
		if (tvec - start >= flushtime)
		{
			fsync(fdscript);
			start = tvec;
		}
		if (Fflg)
			fsync(fdscript);
	}
	finish();
	done(0);
	return (0);
}