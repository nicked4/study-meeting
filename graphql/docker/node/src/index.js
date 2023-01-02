const { ApolloServer, gql } = require('apollo-server');

const users = [
    { id: '1', name: 'John Doe', email: 'john@test.com' },
    { id: '2', name: 'Jane Doe', email: 'jane@example.com' },
  ];

// schema定義
const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    hello(name: String!): String
    users: [User]
    user(id: ID!): User
  }
`;

// resolvers設定
const resolvers = {
    Query: {
      hello: (parent, args) => `Hello ${args.name}`,
      users: () => users,
      user: (parent, args) => {
        const user = users.find((user) => user.id === args.id);
        return user;
      },
    },
  };

// Apollo Server立ち上げ
const server = new ApolloServer({ typeDefs, resolvers });

server.listen().then(({ url }) => {
console.log(`🚀  Server ready at ${url}`);
});