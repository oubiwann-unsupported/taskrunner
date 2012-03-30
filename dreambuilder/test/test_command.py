from twisted.trial import unittest

from dreambuilder import exceptions
from dreambuilder.command import CommandExpression as CExp


complex_commands = CExp(
    CExp("pre-install check",
        CExp("install deps",
            CExp("install a dependency service",
                CExp("start service")
            ),
        ),
        halt_on_fail=True),
    CExp("do primary install",
        CExp("run a parallel process"),
        CExp("run another one"),
        CExp("run a thrid one"),
        CExp("run a fourth one, with a long chain",
            CExp("after 4th, do 4.1",
                CExp("after 4.1, do 4.2",
                    CExp("after 4.2, do 4.3",
                        CExp("after 4.3, do 4.4")
                    )
                )
            )
        ),
        CExp("run a fifth, with a big parallel batch afterwards",
            CExp("batch job 1"),
            CExp("batch job 2"),
            CExp("batch job 3"),
            CExp("batch job 4"),
            CExp("batch job 5"),
            CExp("batch job 6"),
            CExp("batch job 7"),
            CExp("batch job 8"),
            CExp("batch job 9"),
            CExp("batch job 10"),
            CExp("batch job 11"),
            CExp("batch job 12")
        )
    ),
    CExp("post-install check"),
)


class CommandExpressionTestCase(unittest.TestCase):
    """
    """
    def test_simple_command(self):
        simple_command = CExp("do it")
        self.assertEqual(simple_command.command, "do it")

    def test_simple_command_as_parameter(self):
        simple_command = CExp(command="do it")
        self.assertEqual(simple_command.command, "do it")

    def test_two_commands(self):
        double_command = (CExp, "try to do this", "and this")
        self.assertRaises(exceptions.MultipleCommandsError, *double_command)

    def test_two_commands_one_as_parameter(self):
        self.assertRaises(
            exceptions.MultipleCommandsError, 
            lambda: CExp("try to do this", command="and this"))

    def test_no_command(self):
        no_command = CExp()
        self.assertEqual(no_command.command, "")

    def test_command_and_cexp(self):
        simple_nested = CExp("a command", CExp("another command"))
        self.assertEqual(simple_nested.command, "a command")
        self.assertEqual(len(simple_nested.children), 1)
        self.assertEqual(simple_nested.children[0].command, "another command")

    def test_no_command_and_cexp(self):
        no_command_nested = CExp(CExp("nested command"))
        self.assertEqual(no_command_nested.command, "")
        self.assertEqual(len(no_command_nested.children), 1)
        self.assertEqual(
            no_command_nested.children[0].command, "nested command")

    def SKIP_test_many_commands(self):
        def build_commands():
            commands = []
            for i in xrange(10, 1):
                commands.append(CExp("Command number %s" % i))
            return commands

        commands = CExp()
