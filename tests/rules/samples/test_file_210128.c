int	main(int i/*comment in function parameters*/
		, int x)// comment after function declaration
{
	int	num1;
	int	num2;/* comment in function body not at end of line */// comment in fun
	/*
		Multi line comment in function body

	*/
	num1 = 25;
	num2 = 0;
	while (num2 != 25 && num2 != 25/* comment in while */
		&& num1 < 60)
	{
		num2 += 2;
		num1++;
	}
	return (0); // single line comment
}
