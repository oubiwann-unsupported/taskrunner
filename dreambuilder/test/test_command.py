from twisted.trial import unittest

from dreambuilder import exceptions
from dreambuilder.command import CommandExpression as CExp


def complex_commands():
    return CExp(
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

complex_commands_flat = """
pre-install check
do primary install
post-install check
install deps
run a parallel process
run another one
run a thrid one
run a fourth one, with a long chain
run a fifth, with a big parallel batch afterwards
install a dependency service
after 4th, do 4.1
batch job 1
batch job 2
batch job 3
batch job 4
batch job 5
batch job 6
batch job 7
batch job 8
batch job 9
batch job 10
batch job 11
batch job 12
start service
after 4.1, do 4.2
after 4.2, do 4.3
after 4.3, do 4.4
"""


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

    def test_all_kwargs(self):
        command = CExp(
            command="do it! DO IT!!!", halt_on_fail=True, skip=False,
            message="Awwww, ya-yah. We're doing it.")
        self.assertEqual(command.command, "do it! DO IT!!!")
        self.assertEqual(command.halt_on_fail, True)
        self.assertEqual(command.skip, False)
        self.assertEqual(command.message, "Awwww, ya-yah. We're doing it.")

    def test_kwargs_and_command(self):
        command = CExp(
            "do it! DO IT!!!", halt_on_fail=True, skip=False,
            message="Awwww, ya-yah. We're doing it.")
        self.assertEqual(command.command, "do it! DO IT!!!")
        self.assertEqual(command.halt_on_fail, True)
        self.assertEqual(command.skip, False)
        self.assertEqual(command.message, "Awwww, ya-yah. We're doing it.")

    def test_kwargs_and_no_command(self):
        command = CExp(
            halt_on_fail=True, skip=False,
            message="Awwww, ya-yah. We're doing it.")
        self.assertEqual(command.command, "")
        self.assertEqual(command.halt_on_fail, True)
        self.assertEqual(command.skip, False)
        self.assertEqual(command.message, "Awwww, ya-yah. We're doing it.")

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

    def test_many_commands(self):

        def build_commands():
            commands = []
            for i in xrange(1, 11):
                commands.append(CExp("Command number %s" % i))
            return commands

        commands = CExp(
            "go do this mad, mad, mad command",
            build_commands(),
            [CExp("something strange"), CExp("another strange command")],
            CExp("an afterthought command"),
            CExp("an after-afterthought command")
        )
        self.assertEqual(commands.command, "go do this mad, mad, mad command")
        self.assertEqual(len(commands.children), 14)
        self.assertEqual(commands.children[5].command, "Command number 6")
        self.assertEqual(commands.children[10].command, "something strange")
        self.assertEqual(commands.children[13].command,
                         "an after-afterthought command")

    def test_complex_commands(self):

        commands = complex_commands()
        self.assertEqual(commands.command, "")
        self.assertEqual(len(commands.children), 3)
        self.assertEqual(len(commands.children[0].children), 1)
        self.assertEqual(len(commands.children[1].children), 5)
        self.assertEqual(len(commands.children[2].children), 0)
        self.assertEqual(len(commands.children[1].children[4].children), 12)
        self.assertEqual(len(commands.children[1].children[3].children), 1)
        self.assertEqual(len(
            commands.children[1].children[3].children[0].children), 1)
        self.assertEqual(len(
            commands.children[1].children[3].children[0].children[0].children),
            1)
        self.assertEqual(len(
            commands.children[1].children[3].children[0].children[0].
            children[0].children),
            1)
        self.assertEqual(len(
            commands.children[1].children[3].children[0].children[0].
            children[0].children[0].children),
            0)

    def test_get_descendant(self):
        commands = complex_commands()
        self.assertEqual(commands.get_descendant(
            0).command, "pre-install check")
        self.assertEqual(commands.get_descendant(
            0,0).command, "install deps")
        self.assertEqual(commands.get_descendant(
            0,0,0).command, "install a dependency service")
        self.assertEqual(commands.get_descendant(
            0,0,0,0).command, "start service")
        self.assertEqual(commands.get_descendant(
            1).command, "do primary install")
        self.assertEqual(commands.get_descendant(
            1,3).command, "run a fourth one, with a long chain")
        self.assertEqual(commands.get_descendant(
            1,3,0,0,0,0).command, "after 4.3, do 4.4")
        self.assertRaises(
            exceptions.NoDescendantError, commands.get_descendant,
            1,3,0,0,0,0,0)
        self.assertEqual(commands.get_descendant(
            1,4).command, "run a fifth, with a big parallel batch afterwards")
        self.assertEqual(commands.get_descendant(
            1,4,0).command, "batch job 1")
        self.assertEqual(commands.get_descendant(
            1,4,11).command, "batch job 12")
        self.assertEqual(commands.get_descendant(
            2).command, "post-install check")

    def test_has_children(self):
        commands = complex_commands()
        self.assertTrue(commands.has_children())
        self.assertTrue(commands.get_descendant(0).has_children())
        self.assertTrue(commands.get_descendant(1).has_children())
        self.assertTrue(commands.get_descendant(0,0,0).has_children())
        self.assertTrue(commands.get_descendant(1,3,0).has_children())

        self.assertFalse(commands.get_descendant(0,0,0,0).has_children())
        self.assertFalse(commands.get_descendant(1,0).has_children())
        self.assertFalse(commands.get_descendant(1,3,0,0,0,0).has_children())
        self.assertFalse(commands.get_descendant(2).has_children())

    def test_walk(self):
        commands = complex_commands()
        all_children = list(commands.walk())
        self.assertEqual(len(all_children), 28)
        self.assertEqual(
            "\n".join([x.command for x in all_children]).strip(),
            complex_commands_flat.strip())

    def test_parent_attribute(self):
        commands = complex_commands()
        no_parent = 0
        has_parent = 0
        for child in commands.walk():
            if child.parent:
                has_parent += 1
            else:
                no_parent += 1
        self.assertEqual(no_parent, 1)
        self.assertEqual(has_parent, 27)
