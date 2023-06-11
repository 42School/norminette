void foo(int p, char* complicated) {
	switch (p) {
	case 0:
		if (complicated[0] == 'a') {
			if (complicated[1] == 'b') {
	case 1:
		complicated[2] = 'c';
			}
		}
		break;
	}
}
